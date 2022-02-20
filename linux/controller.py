#!/usr/bin/env python3
from linux.helper import *
from linux.world import World
from linux.hud import HUD
from linux.drivers.G920 import G920
from linux.drivers.inputs import InputEventType, InputDevType, InputPacket
from asyncio import Queue
import linux.config as config


class Controller:
    """
    Main Controller of the wizard
    """
    __instance = None
    def __init__(self):
        # References
        self.__world = World.get_instance()
        self.__hud = HUD.get_instance()
        # TODO: merge vehicle and vehicle_ctl
        self.__vehicle = self.__world.vehicle
        self.__vehicle_ctl = carla.VehicleControl()
        # vars
        self.__autopilot:bool = config.autopilot_enabled
        # events handling
        self.__eventsq:Queue = Queue()
        self.__event_handlers:list = [
            lambda data: self.__world.next_weather(), # change weather
            lambda data: self.__world.restart(), # restart world
            None, # toggle info
            None, # toggle camera
            None, # toggle sensor
            None, # toggle help
            lambda data: None, # Decrease Gear
            lambda data: None, # Increate Gear
            self.__update_acc_input, # accelerator
            self.__update_brake_input, # Break
            self.__update_steer_input, # Steer
            lambda data: None, # Clutch
        ]
        # singleton
        if Controller.__instance is None:
            Controller.__instance = self
        else:
            raise Exception("Error: Reinitialization of Controller")


    @staticmethod
    def get_instance():
        if Controller.__instance is None:
            raise Exception("Error: Class Controller not initialized")
        return Controller.__instance


    def register_event(self,event_type:InputEventType,
                       dev:InputDevType=InputDevType.KBD,val:int=0)->None:
        """
        Register the input event into the event queue
        Inputs:
            event_type: What type of actions is required to take
            dev: From which device
            val: Additional data field
        """
        self.__eventsq.put_nowait(InputPacket(event_type,dev,val))


    def handle_events(self):
        """
        Handle events registered in the previous loop
        """
        # TODO: test whether this configuration works
        #       possible problem: event added while in loop, cause it not handled
        while not self.__eventsq.empty():
            pac:InputPacket = self.__eventsq.get_nowait()
            self.__event_handlers[pac.event_type](pac)


    def __update_steer_input(self,data:InputPacket):
        driver:InputDevType = InputDevType.WIZARD if self.__autopilot \
                                                else InputDevType.WHEEL
        if data.dev == driver:
            self.__vehicle_ctl.steer = G920.SteerMap(data.val)


    def __update_brake_input(self, data:InputPacket):
        self.__vehicle_ctl.brake = G920.PedalMap(data.val)


    def __update_acc_input(self, data:InputPacket):
        self.__vehicle_ctl.throttle = G920.PedalMap(data.val)


