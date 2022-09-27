#!/usr/bin/env python3
from wizard import config
from wizard.drivers.BaseWheel import BaseWheel
from wizard.drivers.inputs import InputDevType, WheelKeyType


class G29(BaseWheel):
    # register keymap
    def __init__(self, dev_type: InputDevType):
        # super class
        super().__init__(dev_type)
        self._ctl_key_map: dict = config.g29_key_map
        self.ev_key_map = {
            288: WheelKeyType.CROSS,
            289: WheelKeyType.SQUARE,
            290: WheelKeyType.CIRCLE,
            291: WheelKeyType.TRIANGLE,
            292: WheelKeyType.RSHIFT,
            293: WheelKeyType.LSHIFT,
            294: WheelKeyType.R2,
            295: WheelKeyType.L2,
            296: WheelKeyType.RSB,
            298: WheelKeyType.R3,
            299: WheelKeyType.L3,
        }
        self.ev_abs_map = {
            0: WheelKeyType.STEER,
            2: WheelKeyType.ACC,
            3: WheelKeyType.BRAKE,
            16: WheelKeyType.HPAD,
            17: WheelKeyType.VPAD
        }
        # 1 for key type and 3 for abs type
        self.ev_events: list = [None, self.ev_key_map, None, self.ev_abs_map]
        self._ev_connect()
        self._init()


if __name__ == "__main__":
    rw = G29(InputDevType.WHEEL)
