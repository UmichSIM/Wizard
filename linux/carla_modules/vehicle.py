#!/usr/bin/env python3
import carla
class Vehicle:
    def __init__(self,blueprint, spawn_point):
        from linux.world import World
        self.vehicle:carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)
        self._ctl:carla.VehicleControl = self.vehicle.get_control()

    def destroy(self):
        self.vehicle.destroy()


    def get_transform(self):
        return self.vehicle.get_transform()


    def update(self):
        self.vehicle.apply_control(self._ctl)


    def set_brake(self,val:float):
        self._ctl.brake = val


    def set_throttle(self,val:float):
        self._ctl.throttle = val


    def set_steer(self,val:float):
        self._ctl.steer = val

    def set_reverse(self,val:bool):
        self._ctl.reverse = val


    def get_control(self) -> carla.VehicleControl:
        return self._ctl
