#!/usr/bin/env python3
"""
https://python-evdev.readthedocs.io/en/latest/tutorial.html
Test the ecodes for evdev device
use $(cat /proc/bus/input/devices) to find the event number
"""
import evdev
from evdev import InputDevice, categorize, ecodes
import sys

if __name__ == "__main__":
    # register device
    dev = evdev.InputDevice(sys.argv[1])
    for event in dev.read_loop():
        if event.type == ecodes.EV_ABS and event.code != 1:
            print(event)
