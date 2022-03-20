#!/usr/bin/env python
from wizard import config
from wizard.drivers.BaseWheel import BaseWheel
from wizard.drivers.inputs import InputDevType, WheelKeyType


class G27(BaseWheel):
    # register keymap
    def __init__(self, dev_type: InputDevType):
        # super class
        super().__init__(dev_type)
        self._ctl_key_map:dict = config.g27_key_map
        self.ev_key_map = {
            292: WheelKeyType.RSHIFT,
            293: WheelKeyType.LSHIFT,
            294: WheelKeyType.RTOP,
            295: WheelKeyType.LTOP,
            706: WheelKeyType.RMID,
            707: WheelKeyType.RBOT,
            708: WheelKeyType.LMID,
            709: WheelKeyType.LBOT,
        }
        self.ev_abs_map = {
            0: WheelKeyType.STEER,
            2: WheelKeyType.ACC,
            5: WheelKeyType.BRAKE,
        }
        # 1 for key type and 3 for abs type
        self.ev_events:list = [
        None, self.ev_key_map, None, self.ev_abs_map
    ]
        self._ev_connect()
        self._init()
