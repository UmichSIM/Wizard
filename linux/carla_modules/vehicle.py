#!/usr/bin/env python3
from time import time
import carla
from linux.drivers.inputs import InputDevType, InputPacket
import linux.config as config
from linux.config import UserWheel, WizardWheel

class Vehicle:
    """
    Vehicle class is a wrapper for carla vehicle apis and is combined
    with wizard switching functions. It also owns the drivers for the
    racing wheels. The class is a singleton.
    """
    __instance = None
    def __init__(self,blueprint, spawn_point):
        """
        Inputs:
            blueprint: the model for the vehicle to use
            spawn_point: initial transformation data of the vehicle
        for more information on the input, refer to Carla API documents
        """
        # Singleton
        if Vehicle.__instance is None:
            Vehicle.__instance = self
        else:
            raise Exception("Error: Reinitialization of Vehicle.")

        from linux.world import World
        self.vehicle:carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)
        self._ctl:carla.VehicleControl = carla.VehicleControl()
        self.driver:InputDevType = InputDevType.WHEEL
        self.DriverWheel:type = self.__get_driver_wheel()
        self.enable_wizard:bool = config.enable_wizard
        self.user_wheel:UserWheel = UserWheel(InputDevType.WHEEL)
        if config.enable_wizard:
            self.wizard_wheel:WizardWheel = WizardWheel(InputDevType.WIZARD)


    @staticmethod
    def get_instance():
        if Vehicle.__instance is None:
            raise Exception("Error: Class Vehicle not initialized")
        return Vehicle.__instance

    def start(self):
        self.user_wheel.start()
        if config.enable_wizard:
            self.wizard_wheel.start()

    def change_vehicle(self, blueprint, spawn_point):
        "Using carla api to change the current vehicle"
        from linux.world import World
        self.vehicle.destroy()
        self.vehicle:carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)
        self._ctl:carla.VehicleControl = self.vehicle.get_control()


    def switch_driver(self,data:InputPacket):
        "Switch the current driver, wizard should be enabled"
        assert(self.enable_wizard)
        assert(data.dev == InputDevType.WIZARD or data.dev == InputDevType.WHEEL)
        # react on push
        if data.val != 1: return
        # control can only be claimed but not gived
        if data.dev == self.driver: return
        self.driver = data.dev
        self.DriverWheel = self.__get_driver_wheel()


    def get_transform(self):
        "from carla Vehicle api"
        return self.vehicle.get_transform()


    def get_velocity(self):
        "from carla Vehicle api"
        return self.vehicle.get_velocity()


    def update(self):
        self.vehicle.apply_control(self._ctl)
        self.user_wheel.SetAutoCenter()
        if self.enable_wizard:
            self.wizard_wheel.SetAutoCenter()


    def set_brake(self,data:InputPacket):
        "set the vehicle brake value"
        if data.dev == self.driver:
            self._ctl.brake = self.DriverWheel.PedalMap(data.val)


    def set_throttle(self,data:InputPacket):
        "set the vehicle throttle value"
        if data.dev == self.driver:
            self._ctl.throttle = self.DriverWheel.PedalMap(data.val)

    def set_steer(self,data:InputPacket):
        "set the vehicle steer value"
        if data.dev == self.driver:
            self._ctl.steer = self.DriverWheel.SteerMap(data.val)


    def set_reverse(self,dev:InputDevType, val:bool):
        "Set the inverse mode of the vehicle"
        if dev == self.driver:
            self._ctl.reverse = val


    def get_control(self):
        "From carla api"
        return self._ctl


    def get_driver_name(self) -> str:
        "Get the current driver as string"
        if self.driver == InputDevType.WHEEL:
            return "Human"
        else:
            return "Wizard"


    def __get_driver_wheel(self) -> type:
        if self.driver == InputDevType.WHEEL:
            return UserWheel
        elif self.driver == InputDevType.WIZARD:
            return WizardWheel
        else:
            raise Exception("Invalid driver: {}".format(self.driver))
