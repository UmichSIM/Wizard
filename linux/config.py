#!/usr/bin/env python3
from linux.drivers.inputs import WheelKeyType,ControlEventType
from linux.drivers.G920 import G920
# frame rate for client
client_frame_rate:int = 60
# indicate whether to record the game onto the disk
cam_recording:bool = False
cam_record_dir:str = "./_out"
# Racing Wheel config
wheel1_name = "Logitech G920 Driving Force Racing Wheel"
enable_wizard:bool = False
# The wheel model to use
UserWheel:type = G920
WizardWheel:type = G920

# device event file
user_input_event:str = "/dev/input/event19"
wizard_input_event:str = "/dev/input/event20"

# key maps for user to configure
user_key_map:dict = {
    WheelKeyType.XBOX: ControlEventType.RESTART_WORLD,
    WheelKeyType.VIEW: ControlEventType.TOGGLE_INFO,
    WheelKeyType.MENU: ControlEventType.TOGGLE_HELP,
    WheelKeyType.LSB: ControlEventType.TOGGLE_SENSOR,
    WheelKeyType.RSB: ControlEventType.TOGGLE_CAMERA,
    WheelKeyType.A: ControlEventType.SWITCH_DRIVER,
    WheelKeyType.LSHIFT: ControlEventType.DEC_GEAR,
    WheelKeyType.RSHIFT: ControlEventType.INC_GEAR,
    WheelKeyType.HPAD: ControlEventType.CHANGE_WEATHER,
    WheelKeyType.STEER: ControlEventType.STEER,
    WheelKeyType.BRAKE: ControlEventType.BRAKE,
    WheelKeyType.CLUTCH: ControlEventType.CLUTCH,
    WheelKeyType.ACC: ControlEventType.ACCELERATOR,
}

wizard_key_map:dict = {
    WheelKeyType.XBOX: ControlEventType.RESTART_WORLD,
    WheelKeyType.VIEW: ControlEventType.TOGGLE_INFO,
    WheelKeyType.MENU: ControlEventType.TOGGLE_HELP,
    WheelKeyType.LSB: ControlEventType.TOGGLE_SENSOR,
    WheelKeyType.RSB: ControlEventType.TOGGLE_CAMERA,
    WheelKeyType.A: ControlEventType.SWITCH_DRIVER,
    WheelKeyType.LSHIFT: ControlEventType.DEC_GEAR,
    WheelKeyType.RSHIFT: ControlEventType.INC_GEAR,
    WheelKeyType.HPAD: ControlEventType.CHANGE_WEATHER,
    WheelKeyType.STEER: ControlEventType.STEER,
    WheelKeyType.BRAKE: ControlEventType.BRAKE,
    WheelKeyType.CLUTCH: ControlEventType.CLUTCH,
    WheelKeyType.ACC: ControlEventType.ACCELERATOR,
}
