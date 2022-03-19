#!/usr/bin/env python3
# ref: https://github.com/gvalkov/python-evdev/issues/122

import time
import evdev
from evdev import ecodes, InputDevice, ff

# Find first EV_FF capable event device (that we have permissions to use).
dev = evdev.InputDevice("/dev/input/event20")
center_pos = -10000  # from -32768 to 32767

springs = (ff.Condition * 2)()
for spring in springs:
    spring.right_saturation = 65535
    spring.left_saturation = 65535
    spring.right_coeff = (2 << 14) - 1
    spring.left_coeff = (2 << 14) - 1
    spring.deadband = 0
    spring.center = center_pos

ef_type = ff.EffectType(ff_condition_effect=springs)
effect = ff.Effect(ecodes.FF_SPRING, -1, 16384,
                   ff.Trigger(0, 0),
                   ff.Replay(32768, 0),
                   ef_type)

repeat_count = 1
effect_id = dev.upload_effect(effect)
try:
    dev.write(ecodes.EV_FF, effect_id, repeat_count)
    input("press enter when done")
finally:
    dev.erase_effect(effect_id)
