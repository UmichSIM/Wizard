#!/usr/bin/env python3
from linux.helper import *
from linux.world import World
from linux.hud import HUD
from linux.drivers.G920 import G920
from linux.drivers.inputs import InputEventType, InputDevType, InputPacket
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
        # Racing wheel registration
        self.wheel = G920(InputDevType.WHEEL)
        self.wheel.start()

        # TODO: merge vehicle and vehicle_ctl
        self.__vehicle = self.__world.vehicle
        self.__vehicle_ctl = self.__vehicle.get_control()
        # vars
        self.__autopilot:bool = config.autopilot_enabled
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
            self.__decrease_gear, # Decrease Gear
            self.__increase_gear, # Increate Gear
            self.__update_acc_input, # accelerator
            self.__update_brake_input, # Break
            self.__update_steer_input, # Steer
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


    def tick(self):
        """
        Update all the stuffs in the main loop
        """
        self.handle_events()
        self.__vehicle.apply_control(self.__vehicle_ctl)
        self.wheel.SetAutoCenter()


    def handle_events(self):
        """
        Handle events registered in the previous loop
        """
        # TODO: test whether this configuration works
        #       possible problem: event added while in loop, cause it not handled
        while not self.__eventsq.empty():
            with self.__event_lock:
                pac:InputPacket = self.__eventsq.get_nowait()
            self.__event_handlers[pac.event_type](pac)


    def __update_steer_input(self,data:InputPacket):
        driver:InputDevType = InputDevType.WIZARD if self.__autopilot \
                                                else InputDevType.WHEEL
        if data.dev == driver:
            self.__vehicle_ctl.steer = G920.SteerMap(data.val)
            print(self.__vehicle_ctl.steer)


    def __update_brake_input(self, data:InputPacket):
        self.__vehicle_ctl.brake = G920.PedalMap(data.val)


    def __update_acc_input(self, data:InputPacket):
        self.__vehicle_ctl.throttle = G920.PedalMap(data.val)


    def __decrease_gear(self, data:InputPacket):
        """
        Decrease the gear of the vehicle
        TODO: move to vehicle class
        """
        self.__vehicle_ctl.reverse = True

    def __increase_gear(self, data:InputPacket):
        """
        Increase the gear of the vehicle
        TODO: move to vehicle class
        """
        self.__vehicle_ctl.reverse = False
