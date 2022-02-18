#!/usr/bin/env python3
"""
https://python-evdev.readthedocs.io/en/latest/tutorial.html
Test the ecodes for evdev device
use $(cat /proc/bus/input/devices) to find the event number
"""
import evdev
from evdev import ecodes
# register device
dev = evdev.InputDevice("/dev/input/event6")
for event in dev.read_loop():
    print(event)
