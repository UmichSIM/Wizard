#!/usr/bin/env python3
import carla
import weakref
from wizard.world import World
from wizard.hud import HUD
from wizard.carla_modules.vehicle import Vehicle

class LaneInvasionSensor(object):
    """
    Sensor to detect Lane Invasion

    If Rumble Strip, send rumble() command to driving wheel (only capatible with G920 now).
    It is done by detecting the 'LaneMarkingType' of the rumble strip.
    """
    def __init__(self):
        self.rumble_lanemarkingtype = "SolidSolid"
        # TODO: use official lane marking type
        # self.rumble_lanemarkingtype = carla.?
        self.sensor = None
        self._parent = Vehicle.get_instance().vehicle
        self.hud = HUD.get_instance()
        world = World.get_instance().world
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
        
        if self.rumble_lanemarkingtype in text:
            Vehicle.get_instance().set_collision()