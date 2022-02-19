#!/usr/bin/env python3
from dataclasses import dataclass
from enum import IntEnum

class InputEventType(IntEnum):
    """
    Enum indicating the event requested for controller to handle
    """
    CHANGE_WEATHER = 0,
    RESTART_WORLD = 1,
    TOGGLE_INFO = 2,
    TOGGLE_CAMERA = 3,
    TOGGLE_SENSOR = 4,
    REVERSE_GEAR = 5,
    TOGGLE_HELP = 6,
    ACCELERATOR = 7,
    BREAK = 8,
    STEER = 9,
    CLUTCH = 10


class InputDevType(IntEnum):
    """
    Enum indicating input device type
        KEYBOARD: keyboard input for debug usage
        WHEEL: Driver input
        WIZARD: Wizard input as autopilot
    """
    KEYBOARD = 0,
    WHEEL = 1,
    WIZARD = 2


@dataclass
class InputPacket:
    """
    dataclass carrying data to controller
    """
    event_type:InputEventType
    dev:InputDevType
    val:int
