#!/usr/bin/env python3
"""
Test the spring ff on given wheel
"""
from time import sleep
from wizard import config

if __name__ == "__main__":
    wheel = config.WheelType(config.client_mode)
    step = 100
    val = 0
    while True:
        val+=step
        sleep(0.01)
        if val > 32767:
            val = 32767
            step = -step
        elif val < -32768:
            val = -32768
            step = -step

        wheel.setFF_spring(val)
