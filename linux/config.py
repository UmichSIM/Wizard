#!/usr/bin/env python3
from linux.drivers.inputs import InputDevType, WheelKeyType,ControlEventType
from linux.drivers.G920 import G920
# frame rate for client
client_frame_rate:int = 60
# indicate whether to record the game onto the disk
cam_recording:bool = False
cam_record_dir:str = "./_out"

# this client runs in which mode
client_mode:InputDevType = InputDevType.WHEEL
# The wheel model to use
WheelType = G920
# device event file
user_input_event:str = "/dev/input/event19"

# key maps for user to configure
g920_key_map:dict = {
    # WheelKeyType.XBOX: ControlEventType.RESTART_WORLD, # TODO: recover this
    WheelKeyType.VIEW: ControlEventType.TOGGLE_INFO,
    WheelKeyType.MENU: ControlEventType.TOGGLE_HELP,
    # WheelKeyType.LSB: ControlEventType.TOGGLE_SENSOR,
    WheelKeyType.LSB: ControlEventType.SWITCH_DRIVER,
    WheelKeyType.RSB: ControlEventType.TOGGLE_CAMERA,
    WheelKeyType.LSHIFT: ControlEventType.DEC_GEAR,
    WheelKeyType.RSHIFT: ControlEventType.INC_GEAR,
    WheelKeyType.HPAD: ControlEventType.CHANGE_WEATHER,
    WheelKeyType.STEER: ControlEventType.STEER,
    WheelKeyType.BRAKE: ControlEventType.BRAKE,
    WheelKeyType.CLUTCH: ControlEventType.CLUTCH,
    WheelKeyType.ACC: ControlEventType.ACCELERATOR,
}
