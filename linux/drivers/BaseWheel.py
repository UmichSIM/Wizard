#!/usr/bin/env python
from evdev import ecodes,InputDevice
import math
from abc import ABC
from linux.world import World
from linux.utils.map import LinearMap
from linux.drivers.inputs import InputDevType, WheelKeyType,ControlEventType
from linux import config
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
        if dev_type == InputDevType.WHEEL:
            self._ctl_key_map:dict = config.user_key_map
        else:
            self._ctl_key_map:dict = config.wizard_key_map
        # data
        self.steer_val:int = 0 # steer input [0,65535]
        self.acc_val:int = 0 # accelarator input [0,255]
        self.brake_val:int = 0 # brake input [0,255]
        self.clutch_val:int = 0 # clutch input [0,255]


    def _init(self):
        # init with 0.75 autocenter force
        self._setFF(ecodes.FF_AUTOCENTER, 0.75)
        print("Racing wheel registered")


    def SetAutoCenter(self):
        '''
        Update the auto center force feedback using speed
        '''
        world = World.get_instance()
        v = world.vehicle.get_velocity()
        speed = (3.6 * math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2))

        # speed limit that influences the autocenter
        S2W_THRESHOLD = 90
        if(speed > S2W_THRESHOLD):
            speed = S2W_THRESHOLD
            # autocenterCmd  \in [0,65535]
        autocenterCmd:float = math.sin(speed/S2W_THRESHOLD)

        # send autocenterCmd to the steeringwheel
        self._setFF(ecodes.FF_AUTOCENTER, autocenterCmd)


    def start(self):
        self._thread.start()

    def events_handler(self) -> None:
        '''
        Capture and handle events
        '''
        from linux.controller import Controller
        for event in self._ev.read_loop():
            if event.type in self.ev_type_accepted:
                key_type:WheelKeyType = self.ev_events[event.type].get(event.code)
                event_type:ControlEventType = self._ctl_key_map.get(key_type, ControlEventType.NONE)
                if event_type is not ControlEventType.NONE:
                    Controller.get_instance().register_event(event_type,
                                                    self.dev_type,event.value)


    def _ev_connect(self):
        "Connect to evdev device based on config file"
        if self.dev_type == InputDevType.WHEEL:
            self._ev: evdev.InputDevice = InputDevice(config.user_input_event)
        elif self.dev_type == InputDevType.WIZARD:
            self._ev: evdev.InputDevice = InputDevice(config.wizard_input_event)
        else: assert(False)

    def _setFF(self,ff_type:int, val:float) -> None:
        """
        Set the force feedback

        Input:
        - type: type of the force feedback
          Available Options:
                ecodes.FF_AUTOCENTER
                ecodes.FF_DAMPER
                ecodes.FF_GAIN
                ecodes.FF_FRICTION
                ecodes.FF_RAMP
        - val: float ranging from [0,1]
        """
        assert(val >= 0 and val <= 1)
        self._ev.write(ecodes.EV_FF, ff_type, int(65535*val))


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
