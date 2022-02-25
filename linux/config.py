#!/usr/bin/env python3
from linux.drivers.inputs import InputEventType, WheelKeyType
from linux.drivers.G920 import G920
# frame rate for client
client_frame_rate:int = 60
# indicate whether to record the game onto the disk
cam_recording:bool = False
cam_record_dir:str = "./_out"
# Racing Wheel config
wheel1_name = "Logitech G920 Driving Force Racing Wheel"
enable_wizard:bool = False
UserWheel:type = G920
WizardWheel:type = G920
user_key_map:dict = {
    WheelKeyType.XBOX: InputEventType.RESTART_WORLD,
    WheelKeyType.VIEW: InputEventType.TOGGLE_INFO,
    WheelKeyType.MENU: InputEventType.TOGGLE_HELP,
    WheelKeyType.LSB: InputEventType.TOGGLE_SENSOR,
    WheelKeyType.RSB: InputEventType.TOGGLE_CAMERA,
    WheelKeyType.LSHIFT: InputEventType.DEC_GEAR,
    WheelKeyType.RSHIFT: InputEventType.INC_GEAR,
    WheelKeyType.HPAD: InputEventType.CHANGE_WEATHER,
    WheelKeyType.STEER: InputEventType.STEER,
    WheelKeyType.BRAKE: InputEventType.BRAKE,
    WheelKeyType.CLUTCH: InputEventType.CLUTCH,
    WheelKeyType.ACC: InputEventType.ACCELERATOR,
}
# autopilot when luanch?
autopilot_enabled = False
