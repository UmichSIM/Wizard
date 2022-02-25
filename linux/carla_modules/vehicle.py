#!/usr/bin/env python3
import carla
from linux.drivers.inputs import InputDevType, InputPacket
import linux.config as config
from linux.config import UserWheel, WizardWheel
class Vehicle:
    __instance = None
    def __init__(self,blueprint, spawn_point):
        # Singleton
        if Vehicle.__instance is None:
            Vehicle.__instance = self
        else:
            raise Exception("Error: Reinitialization of Vehicle.")

        from linux.world import World
        self.vehicle:carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)
        self._ctl:carla.VehicleControl = self.vehicle.get_control()
        self.driver:InputDevType = InputDevType.WIZARD if config.autopilot_enabled \
                                                else InputDevType.WHEEL
        self.DriverWheel:type = self.__get_driver_wheel()
        self.enable_wizard:bool = config.enable_wizard
        self.user_wheel:UserWheel = UserWheel(InputDevType.WHEEL)
        self.user_wheel.start()
        if config.enable_wizard:
            self.wizard_wheel:WizardWheel = WizardWheel(InputDevType.WIZARD)
            self.wizard_wheel.start()


    @staticmethod
    def get_instance():
        if Vehicle.__instance is None:
            raise Exception("Error: Class Vehicle not initialized")
        return Vehicle.__instance

    def change_vehicle(self, blueprint, spawn_point):
        "Using carla api to change the current vehicle"
        from linux.world import World
        self.vehicle.destroy()
        self.vehicle:carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)
        self._ctl:carla.VehicleControl = self.vehicle.get_control()

    def switch_driver(self):
        "Switch the current driver, wizard should be enabled"
        assert(self.enable_wizard)
        if self.driver == InputDevType.WHEEL:
            self.driver = InputDevType.WIZARD
        else:
            self.driver = InputDevType.WHEEL
        self.DriverWheel = self.__get_driver_wheel()

    def get_transform(self):
        "from carla Vehicle api"
        return self.vehicle.get_transform()


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


    def get_control(self) -> carla.VehicleControl:
        return self._ctl


    def __get_driver_wheel(self) -> type:
        if self.driver == InputDevType.WHEEL:
            return UserWheel
        elif self.driver == InputDevType.WIZARD:
            return WizardWheel
        else:
            raise Exception("Invalid driver: {}".format(self.driver))
