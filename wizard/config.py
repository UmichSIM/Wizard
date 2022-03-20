#!/usr/bin/env python3
from wizard.drivers.inputs import InputDevType, WheelKeyType,ControlEventType
from wizard.drivers.G920 import G920
from wizard.drivers.G27 import G27
# frame rate for client
client_frame_rate:int = 60
# indicate whether to record the game onto the disk
cam_recording:bool = False
cam_record_dir:str = "./_out"

# this client runs in which mode
client_mode:InputDevType = InputDevType.WHEEL

# The wheel model to use
WheelType = G920
# WheelType = G27

# device event file
user_input_event:str = "/dev/input/event16"

# key maps for user to configure
g920_key_map:dict = {
    # WheelKeyType.XBOX: ControlEventType.RESTART_WORLD, # TODO: recover this
    WheelKeyType.VIEW: ControlEventType.TOGGLE_INFO,
    WheelKeyType.MENU: ControlEventType.TOGGLE_HELP,
    WheelKeyType.X: ControlEventType.CLOSE,
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

g27_key_map:dict = {
    WheelKeyType.LTOP: ControlEventType.CLOSE,
    WheelKeyType.RTOP: ControlEventType.SWITCH_DRIVER,
    WheelKeyType.LMID: ControlEventType.TOGGLE_CAMERA,
    WheelKeyType.RMID: ControlEventType.CHANGE_WEATHER,
    WheelKeyType.LSHIFT: ControlEventType.DEC_GEAR,
    WheelKeyType.RSHIFT: ControlEventType.INC_GEAR,
    WheelKeyType.STEER: ControlEventType.STEER,
    WheelKeyType.BRAKE: ControlEventType.BRAKE,
    WheelKeyType.ACC: ControlEventType.ACCELERATOR,
}
