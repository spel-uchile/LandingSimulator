"""
Created: 4/20/2020
Autor: Elias Obreque Sepulveda
email: els.obrq@gmail.com

"""

import numpy as np


class SlidingControl(object):
    def __init__(self, g, inertia, invinertia, mass, step_mm):
        self.step_width = step_mm/1000
        self.current_time = 0
        self.g = g
        self.Inertia = inertia
        self.mass = mass
        self.invinertia = invinertia
        self.current_error_pos = np.zeros(3)
        self.current_error_vel = np.zeros(3)
        self.current_omega = np.zeros(3)
        self.current_quat = np.zeros(4)
        self.force_ = np.zeros(3)
        self.torque_ = np.zeros(3)
        self.PI = np.diag([1, 1, 1])
        self.PSI = np.diag([2, 2, 2])
        self.sliding_t = np.zeros(3)
        self.sliding_r = np.zeros(3)
        self.k = 10
        self.alpha = 0.5 * np.ones(3)
        self.theta = np.diag([0.01, 0.01, 0.01])
        self.beta = 1
        self.S_quat = np.zeros((3, 3))
        self.time_f = 80

    def set_sliding_t(self):
        self.sliding_t = self.current_error_vel + self.PI.dot(self.current_error_pos)
        return

    def set_sliding_r(self):
        self.sliding_r = self.current_omega + self.k * self.qe_x
        return

    def set_current_state(self, new_position, new_velocity, new_omega, new_quaternion):
        self.current_error_pos = new_position
        self.current_error_vel =  new_velocity
        self.current_omega = new_omega
        self.current_quat = new_quaternion
        self.qe_x = self.current_quat()[0:3]
        self.skewsymmetricmatrix(self.qe_x)
        self.qe_0 = self.current_quat()[3] * np.diag([1, 1, 1])
        self.set_sliding_t()
        self.set_sliding_r()

    def calc_force_torque(self):
        self.force_ = (-self.g - self.PI.dot(self.current_error_vel) - self.PSI.dot(np.sign(self.sliding_t)) - \
                       self.alpha.dot(np.sign(self.sliding_t)))*self.mass
        self.torque_ = -self.invinertia.dot(np.cross(self.current_omega, (self.Inertia.dot(self.current_omega)))) -\
                       0.5 * self.k * (self.S_quat.dot(self.current_omega) + self.qe_0.dot(self.current_omega)) -\
                       self.theta.dot(np.sign(self.sliding_r)) - self.Inertia.dot(self.beta * np.sign(self.sliding_r))
        self.current_time += self.step_width

    def skewsymmetricmatrix(self, x_omega_b):
        self.S_quat[1, 0] = x_omega_b[2]
        self.S_quat[2, 0] = -x_omega_b[1]
        self.S_quat[0, 1] = -x_omega_b[2]
        self.S_quat[0, 2] = x_omega_b[1]

        self.S_quat[2, 1] = x_omega_b[0]
        self.S_quat[1, 2] = -x_omega_b[0]

    def get_force_i(self):
        return self.force_

    def get_torque_b(self):
        return self.torque_
