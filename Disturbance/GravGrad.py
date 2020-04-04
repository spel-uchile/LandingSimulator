import numpy as np


class GravGrad(object):
    def __init__(self, grav_dist_properties):
        self.dist_flag      = grav_dist_properties['gra_calculation']
        self.grav_logging   = grav_dist_properties['gra_logging']
        self.mu_earth = 3.986004418e14
        self.current_grav_torque_b = np.zeros(3)

    def get_torque_b(self):
        return self.current_grav_torque_b

    def update(self, environment, spacecraft):
        self.calc_torque_b(spacecraft.dynamics, spacecraft.dynamics.attitude.Inertia)

    def calc_torque_b(self, r_b, Inertia_b):
        return
