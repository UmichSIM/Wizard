#!/usr/bin/env python3
import evdev
import asyncio
from evdev import ecodes, InputDevice, ff
import math
import config

class RacingWheel:
    def __init__(self,ev_name):
        self.ev_name = ev_name
        # TODO: Change connection type
        self.ev = InputDevice(evdev.list_devices()[0])
        assert(self.ev.name == self.ev_name) # check device name
        self.ev.write(ecodes.EV_FF, ecodes.FF_AUTOCENTER, int(65535*.75))
        print("Racing wheel registered")

    def UpdateFF(self,world):
        '''
        Update the force feedback using speed
        '''
        v = world.player.get_velocity()
        speed = (3.6 * math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2))

        # speed limit that influences the autocenter
        S2W_THRESHOLD = 90
        if(speed > S2W_THRESHOLD):
            speed = S2W_THRESHOLD
            # autocenterCmd  \in [0,65535]
        autocenterCmd = 60000 * math.sin(speed/S2W_THRESHOLD)

        # send autocenterCmd to the steeringwheel
        self.ev.write(ecodes.EV_FF, ecodes.FF_AUTOCENTER, int(autocenterCmd))


    async def events_handler(self):
        '''
        Capture and handle events using asyncio
        '''
        async for event in self.ev.async_read_loop():
            print(self.ev.path, evdev.categorize(event), sep=': ')

if __name__ == "__main__":
    rw = RacingWheel(config.wheel1_name)
    asyncio.ensure_future(rw.events_handler())
    loop = asyncio.get_event_loop()
    loop.run_forever()
