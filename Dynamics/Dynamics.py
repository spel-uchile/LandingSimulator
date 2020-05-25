
from .SpacecraftTrajectory.Trajectory import Trajectory
from .SpacecraftAttitude.Attitude import Attitude
from .CelestialBody.Ephemeris import Ephemeris


class Dynamics(object):
    def __init__(self, dynamics_properties, simtime):
        self.simtime = simtime
        attitude_properties  = {'Omega_b': dynamics_properties['Attitude']['Omega_b'],
                                'Quaternion_i2b': dynamics_properties['Attitude']['Quaternion_i2b'],
                                'Inertia': dynamics_properties['Attitude']['Inertia'],
                                'Mass': dynamics_properties['Attitude']['Mass'],
                                'attitudestep': self.simtime.attitudestep}
        trajectory_properties = {'Orbit_info': dynamics_properties['Orbit']['Orbit_info'],
                                 'propagate': dynamics_properties['Orbit']['propagate'],
                                 'reference_frame': dynamics_properties['Orbit']['reference_frame']}
        self.attitude   = Attitude(attitude_properties)
        self.ephemeris  = Ephemeris(dynamics_properties['Ephemerides'])
        self.trajectory = Trajectory(trajectory_properties, self.simtime.trajectorystep,
                                     self.ephemeris.selected_center_object)

    def update(self):
        self.attitude.update_attitude(self.simtime.maincountTime)
        if self.simtime.trajectory_update_flag:
            self.trajectory.update(self.simtime.get_array_time()[0])
            self.ephemeris.update(self.simtime.current_jd)
            self.trajectory.TransECItoGeo(self.ephemeris.selected_center_object.get_current_sideral())
        self.trajectory.update_attitte(self.attitude.get_class_q_i2b())

    def add_force_b(self, force_b):
        self.trajectory.add_force_b(force_b, self.attitude.get_class_q_b2i(), self.attitude.current_mass)

    def add_force_i(self, force_i):
        self.trajectory.add_force_i(force_i, self.attitude.current_mass)