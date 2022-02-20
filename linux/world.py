#!/usr/bin/env python3
from helper import *
import random
from linux.sensors.CollisionSensor import CollisionSensor
from linux.sensors.LaneInvasionSensor import LaneInvasionSensor
from linux.sensors.GnssSensor import GnssSensor
from linux.sensors.IMUSensor import IMUSensor
from linux.sensors.CameraManager import CameraManager


class World(object):
    """
    Carla world object
    """
    __instance = None
    def __init__(self, carla_world, hud, actor_filter):
        self.world = carla_world
        self.hud = hud
        self.vehicle = None
        self.collision_sensor = None
        self.lane_invasion_sensor = None
        self.gnss_sensor = None
        self.imu_sensor = None
        self.camera_manager = None
        self.__weather_presets = find_weather_presets()
        self.__weather_index = 0
        self.__actor_filter = actor_filter
        # list of actors to be destroyed
        self.__destroy_actors:list = []
        self.restart()
        self.world.on_tick(hud.on_world_tick)
        # Singleton check
        if World.__instance is None:
            World.__instance = self
        else:
            raise Exception("Error: Reinitialization of World")


    @staticmethod
    def get_instance():
        if World.__instance is None:
            raise Exception("Class World not initialized")
        return World.__instance

    def restart(self):
        # Keep same camera config if the camera manager exists.
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_index = self.camera_manager.transform_index if self.camera_manager is not None else 0
        # Get a random blueprint.
        blueprint = random.choice(self.world.get_blueprint_library().filter(self.__actor_filter))
        blueprint.set_attribute('role_name', 'hero')
        if blueprint.has_attribute('color'):
            color = random.choice(blueprint.get_attribute('color').recommended_values)
            blueprint.set_attribute('color', color)
        # Spawn the vehicle.
        if self.vehicle is not None:
            spawn_point = self.vehicle.get_transform()
            spawn_point.location.z += 2.0
            spawn_point.rotation.roll = 0.0
            spawn_point.rotation.pitch = 0.0
            self.destroy()
            self.vehicle = self.world.try_spawn_actor(blueprint, spawn_point)
        while self.vehicle is None:
            spawn_points = self.world.get_map().get_spawn_points()
            spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
            self.vehicle = self.world.try_spawn_actor(blueprint, spawn_point)
            self.register_death(self.vehicle) # register death
        assert(isinstance(self.vehicle, carla.Vehicle))
            # Set up the sensors.
        self.collision_sensor = CollisionSensor(self.vehicle, self.hud)
        self.lane_invasion_sensor = LaneInvasionSensor(self.vehicle, self.hud)
        self.gnss_sensor = GnssSensor(self.vehicle)
        self.imu_sensor = IMUSensor(self.vehicle) #new
        self.camera_manager = CameraManager(self.vehicle, self.hud)
        self.camera_manager.transform_index = cam_pos_index
        self.camera_manager.set_sensor(cam_index, notify=False)
        actor_type = get_actor_display_name(self.vehicle)
        self.hud.notification(actor_type)

    def next_weather(self, reverse=False):
        self.__weather_index += -1 if reverse else 1
        self.__weather_index %= len(self.__weather_presets)
        preset = self.__weather_presets[self.__weather_index]
        self.hud.notification('Weather: %s' % preset[1])
        # TODO: Check whether self.world can be used
        self.vehicle.get_world().set_weather(preset[0])

    def tick(self, clock):
        self.hud.tick(self, clock)

    def render(self, display):
        self.camera_manager.render(display)
        self.hud.render(display)


    def register_death(self,actor):
        """ Register the actors to be destroyed, actor should have destroy method"""
        self.__destroy_actors.append(actor)


    def destroy(self):
        for actor in self.__destroy_actors:
            if actor is not None:
                try:
                    actor.destroy()
                except NameError:
                    print("actor does not have destroy method!")
