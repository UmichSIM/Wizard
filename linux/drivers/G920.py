#!/usr/bin/env python
import evdev
import asyncio
from evdev import ecodes, InputDevice, ff
import config
from linux.drivers.BaseWheel import BaseWheel

class G920(BaseWheel):
    def __init__(self,ev_name):
        self.ev_name = ev_name
        # register events
        self.ev_key_event  = {
            288:self._key_a_handler,
            289:self._key_b_handler,
            290:self._key_x_handler,
            291:self._key_y_handler,
            292:self._key_rshift_handler,
            293:self._key_lshift_handler,
            294:self._key_menu_handler,
            295:self._key_view_handler,
            296:self._key_rsb_handler,
            297:self._key_lsb_handler,
            298:self._key_xbox_handler,
        }
        self.ev_abs_event  = {
            0: self._abs__steer_handler,
            1: self._abs_acc_handler,
            2: self._abs_brake_handler,
            5: self._abs_clutch_handler,
            16: self._abs_pad_handler,
            17: self._abs_pad_handler,
        }
        # TODO: Change connection type
        self.ev:evdev.InputDevice = InputDevice(evdev.list_devices()[0])
        self._init()


if __name__ == "__main__":
    rw = G920(config.wheel1_name)
    asyncio.ensure_future(rw.events_handler())
    loop = asyncio.get_event_loop()
    loop.run_forever()
