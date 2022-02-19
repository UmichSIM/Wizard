#!/usr/bin/env python
from evdev import ecodes
import math
from abc import ABC

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
    def __init__(self):
        # register events
        # evdev device
        self.ev = None
        self.ev_name:str = ""

    def __init(self):
        assert(self.ev.name == self.ev_name) # check device name
        # init with 0.75 autocenter force
        self.__setFF(ecodes.FF_AUTOCENTER, 0.75)
        print("Racing wheel registered")


    def SetAutoCenter(self,world):
        '''
        Update the auto center force feedback using speed
        '''
        v = world.player.get_velocity()
        speed = (3.6 * math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2))

        # speed limit that influences the autocenter
        S2W_THRESHOLD = 90
        if(speed > S2W_THRESHOLD):
            speed = S2W_THRESHOLD
            # autocenterCmd  \in [0,65535]
        autocenterCmd:float = math.sin(speed/S2W_THRESHOLD)

        # send autocenterCmd to the steeringwheel
        self.__setFF(ecodes.FF_AUTOCENTER, autocenterCmd)


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

    def __setFF(self,ff_type:int, val:float) -> None:
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


    def __key_xbox_handler(self,event):
        pass


    def __key_lsb_handler(self,event):
        pass


    def __key_rsb_handler(self,event):
        pass


    def __key_view_handler(self,event):
        pass


    def __key_menu_handler(self,event):
        pass


    def __key_a_handler(self,event):
        pass


    def __key_b_handler(self,event):
        pass


    def __key_x_handler(self,event):
        pass


    def __key_y_handler(self,event):
        pass


    def __key_lshift_handler(self,event):
        """
        handler for left paddle shift on G920
        """
        pass


    def __key_rshift_handler(self,event):
        """
        handler for right paddle shift on G920
        """
        pass


    def __abs__steer_handler(self,event):
        """
        handler for the steering wheel input on G920
        """
        pass


    def __abs_acc_handler(self,event):
        """
        handler for the accelerator input
        """
        pass


    def __abs_brake_handler(self,event):
        """
        handler for the brake input
        """
        pass


    def __abs_clutch_handler(self,event):
        """
        handler for the clutch input
        """
        pass


    def __abs_pad_handler(self,event):
        """
        handler for the directional pad
        c:16 val:-1 -> left
        c:16 val:1 -> right
        c:17 val:-1 -> up
        c:17 val:1 -> down
        """
        pass


    def __sync_event_handler(self, event):
        """
        handler for sync event
        """
