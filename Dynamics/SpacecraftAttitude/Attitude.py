# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 00:17:35 2020

@author: EO
"""

import numpy as np
from Library.math_sup.Quaternion import Quaternions


class Attitude(object):
    def __init__(self, attitude_spacecraft):
        self.attitudestep           = attitude_spacecraft['attitudestep']
        self.attitudecountTime      = 0
        # First time is False to not update the init data
        self.attitude_update_flag   = False

        # quaternion = [i, j, k, 1]
        self.current_quaternion_i2b = Quaternions(attitude_spacecraft['Quaternion_i2b'])

        self.current_omega_b        = np.array(attitude_spacecraft['Omega_b'])

        self.Inertia                = attitude_spacecraft['Inertia']
        self.inv_Inertia            = np.linalg.inv(self.Inertia)

        self.current_h_rw_b     = np.zeros(3)
        self.int_torque_b       = np.zeros(3)
        self.ext_torque_b       = np.zeros(3)
        self.h_total_b          = np.zeros(3)
        self.h_total_i_norm     = 0
        self.new_omega_b        = np.zeros(3)
        self.new_quaternion_i2b = np.zeros(3)
        self.h_total_i          = np.zeros(3)
        self.int_force_b        = np.zeros(3)
        self.ext_force_b        = np.zeros(3)
        self.S_omega            = np.zeros((3, 3))
        self.Omega              = np.zeros((4, 4))
        self.historical_quaternion_i2b = []
        self.historical_omega_b = []
        self.historical_torque_t_b   = []
        self.historical_h_total_i = []

    def update_attitude(self, current_simtime):
        if self.attitude_update_flag:
            while np.abs(current_simtime - self.attitudecountTime - self.attitudestep) > 1e-6:
                self.rungeonestep(self.attitudecountTime, self.attitudestep)
                self.attitudecountTime += self.attitudestep
            self.rungeonestep(self.attitudecountTime, self.attitudestep)
            self.attitudecountTime = current_simtime
        else:
            self.attitude_update_flag = True

        self.calangmom()
        self.reset_var_b()

    def save_attitude_data(self):
        self.historical_quaternion_i2b.append(self.current_quaternion_i2b())
        self.historical_omega_b.append(self.current_omega_b)
        self.historical_torque_t_b.append(self.total_torque_b())
        self.historical_h_total_i.append(self.h_total_i_norm)

    def add_ext_torque_b(self, ext_torque_b):
        self.ext_torque_b += ext_torque_b

    def add_ext_force_b(self, ext_force_b):
        self.ext_force_b += ext_force_b

    def get_ext_force_b(self):
        return self.ext_force_b

    def add_int_torque_b(self, torque_b):
        self.int_torque_b += torque_b

    def add_int_force_b(self, force_b):
        self.int_force_b += force_b

    def get_current_q_i2b(self):
        return self.current_quaternion_i2b()

    def total_torque_b(self):
        return self.ext_torque_b + self.int_torque_b

    def reset_var_b(self):
        self.ext_torque_b = np.zeros(3)
        self.int_torque_b = np.zeros(3)
        self.ext_force_b = np.zeros(3)
        self.int_force_b = np.zeros(3)

    def dynamics_and_kinematics(self, x, t):
        x_omega_b = x[0:3]
        x_quaternion_i2b = x[3:]

        self.skewsymmetricmatrix(x_omega_b)
        self.omega4kinematics(x_omega_b)

        h_total_b = self.current_h_rw_b + self.Inertia.dot(x_omega_b)

        w_dot = -self.inv_Inertia.dot(self.S_omega.dot(h_total_b)
                                      - self.total_torque_b())

        q_dot = 0.5*self.Omega.dot(x_quaternion_i2b)
        f_x = np.concatenate((w_dot, q_dot))
        return f_x

    def rungeonestep(self, t, dt):
        x = np.concatenate((self.current_omega_b, self.current_quaternion_i2b()))
        k1 = self.dynamics_and_kinematics(x, t)
        xk2 = x + (dt / 2.0) * k1

        k2 = self.dynamics_and_kinematics(xk2, (t + dt / 2.0))
        xk3 = x + (dt / 2.0) * k2

        k3 = self.dynamics_and_kinematics(xk3, (t + dt / 2.0))
        xk4 = x + dt * k3

        k4 = self.dynamics_and_kinematics(xk4, (t + dt))

        next_x = x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        self.current_omega_b = next_x[0:3]
        self.current_quaternion_i2b.setquaternion(next_x[3:])
        self.current_quaternion_i2b.normalize()

    def calangmom(self):
        h_spacecraft_b = self.Inertia.dot(self.current_omega_b)
        self.h_total_b = self.current_h_rw_b + h_spacecraft_b
        q_bi2 = Quaternions(self.current_quaternion_i2b.conjugate())
        self.h_total_i = q_bi2.frame_conv(self.h_total_b)
        self.h_total_i_norm = np.linalg.norm(self.h_total_i)

    def skewsymmetricmatrix(self, x_omega_b):

        self.S_omega[1, 0] = x_omega_b[2]
        self.S_omega[2, 0] = -x_omega_b[1]

        self.S_omega[0, 1] = -x_omega_b[2]
        self.S_omega[0, 2] = x_omega_b[1]

        self.S_omega[2, 1] = x_omega_b[0]
        self.S_omega[1, 2] = -x_omega_b[0]

    def omega4kinematics(self, x_omega_b):

        self.Omega[1, 0] = -x_omega_b[2]
        self.Omega[2, 0] = x_omega_b[1]
        self.Omega[3, 0] = -x_omega_b[0]

        self.Omega[0, 1] = x_omega_b[2]
        self.Omega[0, 2] = -x_omega_b[1]
        self.Omega[0, 3] = x_omega_b[0]

        self.Omega[1, 2] = x_omega_b[0]
        self.Omega[1, 3] = x_omega_b[1]

        self.Omega[2, 1] = -x_omega_b[0]
        self.Omega[2, 3] = x_omega_b[2]

        self.Omega[3, 1] = -x_omega_b[1]
        self.Omega[3, 2] = -x_omega_b[2]

    def get_log_values(self):
        report_attitude = {'omega_t_b(X)[rad/s]': np.array(self.historical_omega_b)[:, 0],
                           'omega_t_b(Y)[rad/s]': np.array(self.historical_omega_b)[:, 1],
                           'omega_t_b(Z)[rad/s]': np.array(self.historical_omega_b)[:, 2],
                           'q_t_i2b(0)[-]': np.array(self.historical_quaternion_i2b)[:, 0],
                           'q_t_i2b(1)[-]': np.array(self.historical_quaternion_i2b)[:, 1],
                           'q_t_i2b(2)[-]': np.array(self.historical_quaternion_i2b)[:, 2],
                           'q_t_i2b(3)[-]': np.array(self.historical_quaternion_i2b)[:, 3],
                           'torque_t_b(X)[Nm]': np.array(self.historical_torque_t_b)[:, 0],
                           'torque_t_b(Y)[Nm]': np.array(self.historical_torque_t_b)[:, 1],
                           'torque_t_b(Z)[Nm]': np.array(self.historical_torque_t_b)[:, 2],
                           'h_total[Nms]': np.array(self.historical_h_total_i)}
        return report_attitude
