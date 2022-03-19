#!/usr/bin/env python3
from time import time
import carla
from wizard.drivers.inputs import InputDevType, InputPacket
from wizard import config
from wizard.config import WheelType
from evdev import ecodes

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

        from wizard.world import World
        # user mode, directly create vehicles
        world = World.get_instance()
        if config.client_mode == InputDevType.WHEEL:
            self.vehicle:carla.Vehicle = \
                world.world.try_spawn_actor(blueprint, spawn_point)
            vpc = self.vehicle.get_physics_control()
            vpc.max_rpm-=1 # indicate that the vehicle is controlled manually
            self.vehicle.apply_physics_control(vpc)
            vpc = self.vehicle.get_physics_control()
            print(vpc.max_rpm)
        else: # wizard mode, prompt to choose vehicle
            vehicles = world.world.get_actors().filter('vehicle.*')
            for vehicle in vehicles:
                if vehicle.get_physics_control().max_rpm % 10 != 0:
                    self.vehicle:carla.Vehicle = vehicle

        # control info from agent racing wheel
        self._local_ctl:carla.VehicleControl = carla.VehicleControl()
        # control info from carla server
        self._carla_ctl:carla.VehicleControl = carla.VehicleControl()
        # who is driving
        self.driver:InputDevType = self._get_driver()
        self.joystick_wheel:WheelType = WheelType(config.client_mode)


    @staticmethod
    def get_instance():
        "get the instance of the singleton"
        if Vehicle.__instance is None:
            raise Exception("Error: Class Vehicle not initialized")
        return Vehicle.__instance


    def start(self):
        self.joystick_wheel.start()


    # TODO: recover this
    def change_vehicle(self, blueprint, spawn_point):
        "Using carla api to change the current vehicle"
        from wizard.world import World
        self.vehicle.destroy()
        self.vehicle:carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)


    def switch_driver(self,data:InputPacket):
        "Switch the current driver, wizard should be enabled"
        assert(data.dev == InputDevType.WIZARD or data.dev == InputDevType.WHEEL)
        # react on push
        if data.val != 1: return
        vpc = self.vehicle.get_physics_control()
        # change user
        if self.driver == InputDevType.WIZARD:
            self.driver = InputDevType.WHEEL
            vpc.max_rpm+=1
        else:
            self.driver = InputDevType.WIZARD
            vpc.max_rpm-=1

        self.vehicle.apply_physics_control(vpc)
        # should reinit the control TODO: why?
        # self._ctl = carla.VehicleControl()
        # self.vehicle.apply_control(self._ctl)


    def get_transform(self):
        "from carla Vehicle api"
        return self.vehicle.get_transform()


    def get_velocity(self):
        "from carla Vehicle api"
        return self.vehicle.get_velocity()


    def update(self):
        """
        Update the vehicle status
        """
        self.driver = self._get_driver()
        if self.driver == config.client_mode:
            # update control
            self.vehicle.apply_control(self._local_ctl)
            self._carla_ctl = self._local_ctl
            # erase spring effect
            self.joystick_wheel.erase_ff(ecodes.FF_SPRING)
            # force feedback based on current states
            self.joystick_wheel.SetSpeedFeedback()
        else:
            self._carla_ctl = self.vehicle.get_control()
            # erase auto-center
            self.joystick_wheel.erase_ff(ecodes.FF_AUTOCENTER)
            # force follow
            self.joystick_wheel.SetWheelPos(self._carla_ctl.steer)


    def set_brake(self,data:InputPacket):
        "set the vehicle brake value"
        self._local_ctl.brake = self.joystick_wheel.PedalMap(data.val)


    def set_throttle(self,data:InputPacket):
        "set the vehicle throttle value"
        self._local_ctl.throttle = self.joystick_wheel.PedalMap(data.val)

    def set_steer(self,data:InputPacket):
        "set the vehicle steer value"
        self._local_ctl.steer = self.joystick_wheel.SteerMap(data.val)


    def set_reverse(self,dev:InputDevType, val:bool):
        "Set the inverse mode of the vehicle"
        self._local_ctl.reverse = val


    def get_control(self):
        "From carla api"
        return self._carla_ctl


    def _get_driver(self) -> InputDevType:
        "Get the current driver"
        vpc = self.vehicle.get_physics_control()
        if vpc.max_rpm % 10 == 9:
            return InputDevType.WHEEL
        elif vpc.max_rpm % 10 == 8:
            return InputDevType.WIZARD
        else:
            raise Exception("Invalid max_rpm: {}".format(vpc.max_rpm))


    def get_driver_name(self) -> str:
        "Get the current driver as string"
        if self.driver == InputDevType.WHEEL:
            return "Human"
        else:
            return "Wizard"
