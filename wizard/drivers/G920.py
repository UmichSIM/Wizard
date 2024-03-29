#!/usr/bin/env python
from wizard import config
from wizard.drivers.BaseWheel import BaseWheel
from wizard.drivers.inputs import InputDevType, WheelKeyType
from evdev import ecodes, ff


class G920(BaseWheel):
    # register keymap
    def __init__(self, dev_type: InputDevType):
        # super class
        super().__init__(dev_type)
        self._ctl_key_map: dict = config.g920_key_map
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
        self.ev_events: list = [
            None, self.ev_key_map, None, self.ev_abs_map
        ]
        
        self._ev_connect()
        self._init()
        
        rumble = ff.Rumble(strong_magnitude=0xffff, weak_magnitude=0xffff)
        collision_effect = ff.Effect(
            ecodes.FF_RUMBLE, -1, 0,
            ff.Trigger(0, 0),
            ff.Replay(100, 0),
            ff.EffectType(ff_rumble_effect=rumble)
        )
        self.collision_effect_id = self._ev.upload_effect(collision_effect)

    def collision_effect(self):
        self._ev.write(ecodes.EV_FF, self.collision_effect_id, 1)

    def rumble_start(self):
        rumble_duration = 100000
        rumble = ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0xffff)
        rumble_effect = ff.Effect(
            ecodes.FF_RUMBLE, -1, 0,
            ff.Trigger(0, 0),
            ff.Replay(rumble_duration, 0),
            ff.EffectType(ff_rumble_effect=rumble)
        )
        self.rumble_effect_id = self._ev.upload_effect(rumble_effect)
        self._ev.write(ecodes.EV_FF, self.rumble_effect_id, 1)

    def rumble_stop(self):
        self._ev.erase_effect(self.rumble_effect_id)

if __name__ == "__main__":
    rw = G920(InputDevType.WHEEL)
