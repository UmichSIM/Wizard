#!/usr/bin/env python3
from dataclasses import dataclass
from enum import IntEnum, auto
from linux.controller import ControlEventType

class InputDevType(IntEnum):
    """
    Enum indicating input device type
        KEYBOARD: keyboard input for debug usage
        WHEEL: Driver input
        WIZARD: Wizard input as autopilot
    """
    KBD = 0
    WHEEL = 1
    WIZARD = 2


class WheelKeyType(IntEnum):
    "Enum indicating the keys on the racing wheel"
    XBOX = 0
    LSB = auto(); RSB = auto()
    LSHIFT = auto(); RSHIFT = auto()
    VIEW = auto(); MENU = auto()
    A = auto(); B = auto(); X = auto(); Y = auto();
    HPAD = auto(); VPAD = auto() # pads in horizon and vertical
    STEER = auto(); CLUTCH = auto(); BRAKE = auto(); ACC = auto()



@dataclass
class InputPacket:
    """
    dataclass carrying data to controller
    """
    event_type:ControlEventType
    dev:InputDevType
    val:int
