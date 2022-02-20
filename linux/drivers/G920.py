#!/usr/bin/env python
import evdev
import asyncio
from evdev import ecodes, InputDevice, ff
import config
from linux.drivers.BaseWheel import BaseWheel
from linux.drivers.inputs import InputDevType, WheelKeyType

class G920(BaseWheel):
    # register keymap
    ev_key_map = {
        288: WheelKeyType.A,
        289: WheelKeyType.B,
        290: WheelKeyType.X,
        291: WheelKeyType.Y,
        292: WheelKeyType.RSHIFT,
        293: WheelKeyType.LSHIFT,
        294: WheelKeyType.MENU,
        295: WheelKeyType.VIEW,
        296: WheelKeyType.RSB,
        297: WheelKeyType.LSB,
        298: WheelKeyType.XBOX,
    }
    ev_abs_map = {
        0: WheelKeyType.STEER,
        1: WheelKeyType.ACC,
        2: WheelKeyType.BRAKE,
        5: WheelKeyType.CLUTCH,
        16: WheelKeyType.HPAD,
        17: WheelKeyType.VPAD
    }
    def __init__(self, dev_type:InputDevType):
        # super class
        super().__init__(dev_type)
        # give control key map
        self._ctl_key_map = config.wheel1_key_map
        # TODO: Change connection type
        self.ev:evdev.InputDevice = InputDevice(evdev.list_devices()[0])
        self._init()


if __name__ == "__main__":
    rw = G920(InputDevType.WHEEL)
    asyncio.ensure_future(rw.events_handler())
    loop = asyncio.get_event_loop()
    loop.run_forever()
