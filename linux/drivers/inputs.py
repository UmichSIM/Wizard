#!/usr/bin/env python3
from dataclasses import dataclass
from enum import IntEnum, auto

class InputEventType(IntEnum):
    """
    Enum indicating the event requested for controller to handle
    """
    CHANGE_WEATHER = 0
    RESTART_WORLD = auto()
    TOGGLE_INFO = auto()
    TOGGLE_CAMERA = auto()
    TOGGLE_SENSOR = auto()
    TOGGLE_HELP = auto()
    DEC_GEAR = auto()
    INC_GEAR = auto()
    ACCELERATOR = auto()
    BRAKE = auto()
    STEER = auto()
    CLUTCH = auto()
    NONE = auto() # do nothing


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
