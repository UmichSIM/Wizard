#!/usr/bin/env python3
"""
Test the spring ff on given wheel
"""
from time import sleep
from wizard import config

if __name__ == "__main__":
    wheel = config.WheelType(config.client_mode)
    step = 0.005
    val = 0
    while True:
        val+=step
        sleep(0.01)
        if val > 1:
            val = 1
            step = -step
        elif val < -1:
            val = -1
            step = -step

        wheel.SetWheelPos(val)
