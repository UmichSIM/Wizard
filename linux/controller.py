#!/usr/bin/env python3
from linux.helper import *
from linux.world import World
from linux.hud import HUD
from linux.drivers.G920 import G920
from linux.drivers.inputs import InputEventType, InputDevType, InputPacket
from linux.carla_modules.vehicle import Vehicle
from threading import Lock
from queue import Queue
import linux.config as config
import carla


class Controller:
    """
    Main Controller of the wizard
    """
    __instance = None
    def __init__(self):
        # singleton
        if Controller.__instance is None:
            Controller.__instance = self
        else:
            raise Exception("Error: Reinitialization of Controller")
        # objects and references
        self.__world = World.get_instance()
        self.__hud = HUD.get_instance()

        self.__vehicle:Vehicle = Vehicle.get_instance()
        # vars
        self.driver:InputDevType = InputDevType.WIZARD if config.autopilot_enabled \
                                                else InputDevType.WHEEL

        # events handling
        self.__event_lock:Lock = Lock()
        self.__eventsq:Queue = Queue()
        self.__event_handlers:list = [
            lambda data: self.__world.next_weather(), # change weather
            lambda data: self.__world.restart(), # restart world
            lambda data: self.__hud.toggle_info(), # toggle info
            lambda data: self.__world.camera_manager.toggle_camera(), # toggle camera
            lambda data: self.__world.camera_manager.next_sensor(), # toggle sensor
            lambda data: self.__hud.help.toggle(), # toggle help
            lambda data: self.__vehicle.set_reverse(data.dev, False), # Decrease Gear
            lambda data: self.__vehicle.set_reverse(data.dev, True), # Increate Gear
            self.__vehicle.set_throttle, # Accelerator
            self.__vehicle.set_brake, # Brake
            self.__vehicle.set_steer, # Steer
            lambda data: None, # Clutch
        ]
        


    @staticmethod
    def get_instance():
        if Controller.__instance is None:
            Controller.__instance = Controller()
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
        with self.__event_lock:
            self.__eventsq.put_nowait(InputPacket(event_type,dev,val))


    def tick(self,clock):
        """
        Update all the stuffs in the main loop
        """
        self.handle_events()
        self.__vehicle.update()
        self.__hud.tick(clock)


    def handle_events(self):
        """
        Handle events registered in the previous loop
        """
        while not self.__eventsq.empty():
            with self.__event_lock:
                pac:InputPacket = self.__eventsq.get_nowait()
            self.__event_handlers[pac.event_type](pac)
