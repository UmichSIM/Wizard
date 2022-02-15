#!/usr/bin/env python
import evdev
import asyncio
from evdev import ecodes, InputDevice, ff
import math
import config
from abc import ABC
from BaseWheel import BaseWheel

class G920(BaseWheel):
    def __init__(self,ev_name):
        self.ev_name = ev_name
        # register events
        # TODO: register keys
        self.ev_sync_event  = {}
        self.ev_key_event  = {}
        self.ev_abs_event  = {}
        # TODO: Change connection type
        self.ev = InputDevice(evdev.list_devices()[0])
        self.__init()


if __name__ == "__main__":
    rw = RacingWheel(config.wheel1_name)
    asyncio.ensure_future(rw.events_handler())
    loop = asyncio.get_event_loop()
    loop.run_forever()
