#!/usr/bin/env python
from wizard import config
from wizard.drivers.BaseWheel import BaseWheel
from wizard.drivers.inputs import InputDevType, WheelKeyType


class G920(BaseWheel):
    # register keymap
    def __init__(self, dev_type: InputDevType):
        # super class
        super().__init__(dev_type)
        self._ctl_key_map:dict = config.g920_key_map
        self.ev_key_map = {
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
        self.ev_abs_map = {
            0: WheelKeyType.STEER,
            1: WheelKeyType.ACC,
            2: WheelKeyType.BRAKE,
            5: WheelKeyType.CLUTCH,
            16: WheelKeyType.HPAD,
            17: WheelKeyType.VPAD
        }
        # 1 for key type and 3 for abs type
        self.ev_events:list = [
        None, self.ev_key_map, None, self.ev_abs_map
    ]
        self._ev_connect()
        self._init()


if __name__ == "__main__":
    rw = G920(InputDevType.WHEEL)
