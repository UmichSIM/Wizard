#!/usr/bin/env python3
import carla
import weakref
from linux.world import World
from linux.hud import HUD
from linux.carla_modules.vehicle import Vehicle

class LaneInvasionSensor(object):
    """
    Sensor to detect Lane Invasion
    """
    def __init__(self):
        self.sensor = None
        self._parent = Vehicle.get_instance().vehicle
        self.hud = HUD.get_instance()
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
        self.sensor = world.spawn_actor(bp, carla.Transform(), attach_to=self._parent)
        World.get_instance().register_death(self.sensor)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: LaneInvasionSensor._on_invasion(weak_self, event))

    @staticmethod
    def _on_invasion(weak_self, event):
        self = weak_self()
        if not self:
            return
        lane_types = set(x.type for x in event.crossed_lane_markings)
        text = ['%r' % str(x).split()[-1] for x in lane_types]
        self.hud.notification('Crossed line %s' % ' and '.join(text))
