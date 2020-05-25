import numpy as np


class GravGrad(object):
    def __init__(self, grav_dist_properties, spacecraft):
        self.dist_flag      = grav_dist_properties['gra_calculation']
        self.dist_logging   = grav_dist_properties['gra_logging']
        self.mu = spacecraft.dynamics.ephemeris.selected_center_object.mu
        self.current_torque_b = np.zeros(3)
        self.historical_torque_b = []

    def get_torque_b(self):
        return self.current_torque_b

    def get_force_b(self):
        return np.zeros(3)

    def update(self, environment, spacecraft):
        self.calc_torque_b(spacecraft.dynamics.trajectory.current_position, spacecraft.dynamics.attitude.Inertia)

    def calc_torque_b(self, R_b, Inertia_b):
        r_b_norm = np.linalg.norm(R_b)
        self.current_torque_b = 3.0 * self.mu / r_b_norm ** 5 * np.cross(R_b, Inertia_b.dot(R_b))

    def save_date(self):
        self.historical_torque_b.append(self.current_torque_b)

    def create_report(self):
        report = {'Grav_torque_b_X': np.array(self.historical_torque_b)[:, 0],
                  'Grav_torque_b_Y': np.array(self.historical_torque_b)[:, 1],
                  'Grav_torque_b_Z': np.array(self.historical_torque_b)[:, 2]}
        return report

