"""
Created: 4/8/2020
Autor: Elias Obreque Sepulveda
email: els.obrq@gmail.com

"""

from .ComponentBase import ComponentBase
from ..Logic.Control.SlidingControl import SlidingControl
from Spacecraft.Components import Components
from Library.math_sup.Quaternion import Quaternions
import numpy as np


class ODCS(ComponentBase):
    def __init__(self, init_componenets, subsystem_setting, dynamics):
        ComponentBase.__init__(self, (1000 / subsystem_setting['ODCS_com_frequency']))
        self.dynamics = dynamics
        self.ctrl_cycle = 1000 / subsystem_setting['ODCS_com_frequency']
        self.port_id = subsystem_setting['port_id']
        self.components = Components(init_componenets, self.dynamics, self.port_id)
        self.current_omega_c_gyro = np.zeros(3)
        self.current_position_i = np.zeros(3)
        self.current_velocity_i = np.zeros(3)
        self.force_thruster_i = np.array([0.0, 0.0, 0.0])
        self.force_thruster_b = np.array([0.0, 0.0, 0.0])
        self.torque_thruster_b = np.zeros(3)
        self.target_position = np.zeros(3)
        self.target_velocity = np.zeros(3)
        self.q_i2b_est = Quaternions([0, 0, 0, 1])
        self.q_b2b_now2tar = Quaternions([0, 0, 0, 1])
        self.q_i2b_tar = Quaternions([0, 0, 0, 1])
        self.ctrl_ang = np.pi/4
        self.mag_thrust = 0
        self.control_torque_b = np.zeros(3)
        self.control_force_i = np.zeros(3)
        self.historical_control_torque_b = []
        self.historical_control_force_i = []
        self.historical_thruster_i = []
        self.g = np.array([0, 0, -1.62])
        self.sliding = SlidingControl(self.g, self.dynamics.attitude.Inertia,
                                      self.dynamics.attitude.inv_Inertia,
                                      self.dynamics.attitude.current_mass,
                                      self.ctrl_cycle)
        for thr in self.components.thruster:
            thr.set_step_width(self.ctrl_cycle / 1000)
            #thr.set_max_thrust(300)
            #thr.set_burn_time(10)

    def main_routine(self, count):

        self.read_sensors()

        self.determine_attitude()

        self.determine_orbit()

        self.check_mode()

        self.calculate_control_force_torque()

        self.calc_thruster_force_i()
        return

    def read_sensors(self):
        self.current_omega_c_gyro = self.components.gyro.measure(self.dynamics.attitude.current_omega_b)
        self.current_position_i = self.dynamics.trajectory.current_position
        self.current_velocity_i = self.dynamics.trajectory.current_velocity

    def determine_attitude(self):
        att = self.dynamics.attitude.get_current_q_i2b()
        self.q_i2b_est.setquaternion(att)
        return

    def determine_orbit(self):
        return

    def check_mode(self):
        # Vector direction of the Body frame to point to another vector
        b_dir = np.array([0, 0, 1])

        # Vector target from Inertial frame
        i_tar = np.array([0, 0, 1])
        i_tar = i_tar / np.linalg.norm(i_tar)

        # Vector target from body frame
        b_tar = self.q_i2b_est.frame_conv(i_tar)

        b_lambda = np.cross(b_dir, b_tar)
        rot = np.arcsin(np.linalg.norm(b_lambda) / (np.linalg.norm(b_tar) * np.linalg.norm(b_dir)))

        self.q_b2b_now2tar.setquaternion([b_lambda, rot])
        self.q_b2b_now2tar.normalize()
        self.q_i2b_tar = self.q_i2b_est * self.q_b2b_now2tar
        return

    def calculate_control_force_torque(self):
        q_b2i_est = Quaternions(self.q_i2b_est.conjugate())
        # First it is necessary to pass the quaternion from attitude to inertial,
        # then the target vector is rotated from the inertial to body frame
        q_i2b_now2tar = q_b2i_est * self.q_i2b_tar
        q_i2b_now2tar.normalize()
        omega_b_tar = np.zeros(3)

        error_omega = omega_b_tar - self.dynamics.attitude.current_omega_b
        error_vel = self.dynamics.trajectory.current_velocity - np.zeros(3)
        error_pos = self.dynamics.trajectory.current_position - np.zeros(3)
        self.sliding.set_current_state(error_pos,
                                       error_vel,
                                       error_omega,
                                       q_i2b_now2tar)
        self.sliding.calc_force_torque()
        self.control_force_i = self.sliding.get_force_i()
        self.torque_thruster_b = self.sliding.get_torque_b()
        return

    def calc_thruster_force_b(self):
        for thr in self.components.thruster:
            thr.set_thrust_i(self.control_force_i / len(self.components.thruster))
            thr.calc_thrust_and_torque_b(self.q_i2b_est)
        self.torque_thruster_b = self.control_force_i

    def calc_thruster_force_i(self):
        thruster_force_i = 0
        for thr in self.components.thruster:
            thr.set_thrust_i(self.control_force_i / len(self.components.thruster))
            thr.calc_thrust_and_torque_i(self.ctrl_cycle)
            thruster_force_i += thr.get_force_i()
        self.force_thruster_i = thruster_force_i

    def get_force_b(self):
        return self.force_thruster_b

    def get_force_i(self):
        return self.control_force_i

    def get_torque_b(self):
        return self.torque_thruster_b

    def log_value(self):
        self.historical_control_torque_b.append(self.control_torque_b)
        self.historical_control_force_i.append(self.control_force_i)
        self.historical_thruster_i.append(self.force_thruster_i)
        return

    def get_log_values(self):
        report = {'Control_X_i [N]': np.array(self.historical_control_force_i)[:, 0],
                  'Control_Y_i [N]': np.array(self.historical_control_force_i)[:, 1],
                  'Control_Z_i [N]': np.array(self.historical_control_force_i)[:, 2],
                  'Thruster_X_i [N]': np.array(self.historical_thruster_i)[:, 0],
                  'Thruster_Y_i [N]': np.array(self.historical_thruster_i)[:, 1],
                  'Thruster_Z_i [N]': np.array(self.historical_thruster_i)[:, 2]}
        return report