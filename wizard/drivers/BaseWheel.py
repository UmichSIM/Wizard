#!/usr/bin/env python
from evdev import ecodes,InputDevice, ff
import math
from abc import ABC
from wizard.utils.map import LinearMap
from wizard.drivers.inputs import InputDevType, WheelKeyType,ControlEventType
from wizard import config
import threading


class BaseWheel(ABC):
    """
    Abstract wheel class to be inherited
    """
    
    # settings
    steer_max:int = 65535 # max possible value to steering wheel
    pedal_max:int = 255 # max possible value of pedals
    def __init__(self, dev_type:InputDevType = InputDevType.WHEEL):
        # static variables
        self.ev_key_map:dict = {}
        self.ev_abs_map:dict = {}
        # 1 for key type and 3 for abs type
        self.ev_events:list = [
    ]
        self.ev_type_accepted:tuple = (1,3)

        # thread
        self._thread =threading.Thread(target=self.events_handler)
        # type
        self.dev_type:InputDevType = dev_type
        # evdev device
        self._ev = None
        self._ctl_key_map:dict = {}
        # data
        self.steer_val:int = 0 # steer input [0,65535]
        self.acc_val:int = 0 # accelarator input [0,255]
        self.brake_val:int = 0 # brake input [0,255]
        self.clutch_val:int = 0 # clutch input [0,255]
        # FF id
        self._ff_spring_id = None


    def __del__(self):
        "Destructor, used to erase ff settings"
        self._ev.close()

    def _init(self):
        # init with 49150 autocenter force
        # self._setFF(ecodes.FF_AUTOCENTER, 49150)
        print("Racing wheel registered")


    def SetAutoCenter(self):
        '''
        Update the auto center force feedback using speed
        '''
        from wizard.carla_modules.vehicle import Vehicle
        v = Vehicle.get_instance().get_velocity()
        speed = (3.6 * math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2))

        # speed limit that influences the autocenter
        S2W_THRESHOLD = 90
        if(speed > S2W_THRESHOLD):
            speed = S2W_THRESHOLD
            # autocenterCmd  \in [0,65535]
        autocenterCmd:int = int(math.sin(speed/S2W_THRESHOLD)*65535)

        # send autocenterCmd to the steeringwheel
        self._setFF(ecodes.FF_AUTOCENTER, autocenterCmd)


    def start(self):
        self._thread.start()

    def events_handler(self) -> None:
        '''
        Capture and handle events
        '''
        from wizard.controller import Controller
        for event in self._ev.read_loop():
            if event.type in self.ev_type_accepted:
                key_type:WheelKeyType = self.ev_events[event.type].get(event.code)
                event_type:ControlEventType = self._ctl_key_map.get(key_type, ControlEventType.NONE)
                if event_type is not ControlEventType.NONE:
                    Controller.get_instance().register_event(event_type,
                                                    self.dev_type,event.value)


    def _ev_connect(self):
        "Connect to evdev device based on config file"
        self._ev: evdev.InputDevice = InputDevice(config.user_input_event)

    def _setFF(self,ff_type:int, val:int) -> None:
        """
        Set the force feedback

        Input:
        - type: type of the force feedback
          Available Options:
                ecodes.FF_AUTOCENTER
                ecodes.FF_DAMPER
                ecodes.FF_GAIN
                ecodes.FF_FRICTION
                ecodes.FF_SPRING
                ecodes.FF_RAMP
        - val: int ranging from [0,65535] or [-32768,32767]
        """
        if ff_type == ecodes.FF_SPRING:
            self.setFF_spring(val)
            return
        assert(val >= 0 and val <= 65535)
        self._ev.write(ecodes.EV_FF, ff_type, val)

    def setFF_spring(self, pos:int, right_saturation:int = 65535,
                      left_saturation:int = 65535, right_coeff = 32767,
                      left_coeff = 32767, deadband = 0) -> None:
        """
        Set the spring force feedback
        Input:
        - pos: position of the balance point
        - right_saturation: maximum level when wheel moved all way to right
        - left_saturation: same for the left side
        - right_coeff: controls how fast the force grows when the joystick
                       moves to the right
        - left_coeff: same for the left side
        - deadband: size of the dead zone, where no force is produced
        """
        # create effect
        springs = (ff.Condition * 2)()
        for spring in springs:
            spring.right_saturation = right_saturation
            spring.left_saturation = left_saturation
            spring.right_coeff = right_coeff
            spring.left_coeff = left_coeff
            spring.deadband = deadband
            spring.center = pos

        # register effect
        spring_id = self._ev.upload_effect(
                ff.Effect(ecodes.FF_SPRING, -1, 16384,
                          ff.Trigger(0,0),
                          ff.Replay(32768,0),
                          ff.EffectType(ff_condition_effect = springs)))

        self._ev.write(ecodes.EV_FF, spring_id, 1)

        # erase previous eefect
        if self._ff_spring_id is not None:
            self._ev.erase_effect(self._ff_spring_id)

        self._ff_spring_id = spring_id


    @classmethod
    def SteerMap(cls,val:int):
        """
        map the input of steering wheel to carla defined region [-1,1]
        """
        return LinearMap(val,cls.steer_max)*2-1


    @classmethod
    def PedalMap(cls,val:int):
        """
        map the input of pedals to carla defined region [0,1]
        """
        # reverse the input because 255 is 0 in evdev
        return LinearMap(cls.pedal_max - val,cls.pedal_max)
