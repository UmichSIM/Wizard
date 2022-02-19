#!/usr/bin/env python
from evdev import ecodes
import math
from abc import ABC
from linux.world import World
from linux.utils.map import LinearMap


class BaseWheel(ABC):
    """
    Abstract wheel class to be inherited
    """
    # static variables
    ev_key_event:dict = {}
    ev_abs_event:dict = {}
    ev_type_accepted:tuple = (1,3)
    ev_events:list = [None,
                      ev_key_event,
                      None,
                      ev_abs_event]
    # settings
    steer_max:int = 65535 # max possible value to steering wheel
    pedal_max:int = 255 # max possible value of pedals
    def __init__(self):
        # register events
        # evdev device
        self.ev = None
        self.name:str = ""
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


    async def events_handler(self) -> None:
        '''
        Capture and handle events using asyncio
        '''
        async for event in self.ev.async_read_loop():
            try:
                if event.type in self.ev_type_accepted:
                    self.ev_events[event.type][event.code](event)
            except:
                raise Exception(
                    "No handler for code {0} in type {1}".format(event.code, event.type))

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
        self.ev.write(ecodes.EV_FF, ff_type, int(65535*val))


    def _key_xbox_handler(self,event):
        pass


    def _key_lsb_handler(self,event):
        pass


    def _key_rsb_handler(self,event):
        pass


    def _key_view_handler(self,event):
        pass


    def _key_menu_handler(self,event):
        pass


    def _key_a_handler(self,event):
        pass


    def _key_b_handler(self,event):
        pass


    def _key_x_handler(self,event):
        pass


    def _key_y_handler(self,event):
        pass


    def _key_lshift_handler(self,event):
        """
        handler for left paddle shift on G920
        """
        pass


    def _key_rshift_handler(self,event):
        """
        handler for right paddle shift on G920
        """
        pass


    def _abs__steer_handler(self,event):
        """
        handler for the steering wheel input on G920
        """
        self.steer_val = event.value


    def _abs_acc_handler(self,event):
        """
        handler for the accelerator input
        """
        self.acc_val = event.value


    def _abs_brake_handler(self,event):
        """
        handler for the brake input
        """
        self.brake_val = event.value


    def _abs_clutch_handler(self,event):
        """
        handler for the clutch input
        """
        self.clutch_val = event.value


    def _abs_pad_handler(self,event):
        """
        handler for the directional pad
        c:16 val:-1 -> left
        c:16 val:1 -> right
        c:17 val:-1 -> up
        c:17 val:1 -> down
        """
        pass


    @classmethod
    def SteerMap(cls,val:int):
        """
        map the input of steering wheel to carla defined region [-1,1]
        """
        return LinearMap(val,cls.steer_max)


    @classmethod
    def PedalMap(cls,val:int):
        """
        map the input of pedals to carla defined region [0,1]
        """
        # reverse the input because 255 is 0 in evdev
        return LinearMap(cls.steer_max - val,cls.steer_max)
