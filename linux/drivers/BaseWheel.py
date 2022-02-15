#!/usr/bin/env python
import evdev
import asyncio
from evdev import ecodes, InputDevice, ff
import math
from linux import config
from abc import ABC

class BaseWheel(ABC):
    """
    Abstract wheel class to be inherited
    """
    def __init__(self):
        # register events
        # TODO: register keys
        self.ev_sync_event:dict = {}
        self.ev_key_event:dict = {}
        self.ev_abs_event:dict = {}
        self.ev_events = [self.ev_sync_event,
                          self.ev_key_event,
                          None,
                          self.ev_abs_event]
        # evdev device
        self.ev:evdev.InputDevice = None

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


    async def events_handler(self) -> int:
        '''
        Capture and handle events using asyncio
        '''
        async for event in self.ev.async_read_loop():
            print(self.ev.path, evdev.categorize(event), sep=': ')

        return 0

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
