
from .ComponentBase import ComponentBase
from Spacecraft.Components import Components
from Library.math_sup.Quaternion import Quaternions
import numpy as np


class ADCS(ComponentBase):
    def __init__(self, init_componenets, subsystem_setting, dynamics):
        # prescalar_time in [ms]
        ComponentBase.__init__(self, prescalar_time=(1000 / subsystem_setting['ADCS_com_frequency']))
        # component quaternion
        self.q_b2c = subsystem_setting['q_b2c']
        # cycle in [ms]
        self.ctrl_cycle = 1000 / subsystem_setting['ADCS_com_frequency']
        self.port_id = subsystem_setting['port_id']
        self.comp_number = subsystem_setting['ADCS_COMPONENT_NUMBER']
        self.dynamics = dynamics
        self.components = Components(init_componenets, self.dynamics, self.port_id)
        self.current_omega_c_gyro = np.zeros(3)
        self.torque_rw_b = np.zeros(3)
        self.error_int = 0
        self.omega_b_est = np.zeros(3)
        self.control_torque = np.zeros(3)
        self.P_omega = subsystem_setting['P_omega']
        self.I_quat = subsystem_setting['I_quat']
        self.P_quat = subsystem_setting['P_quat']
        self.rw_torque_b = np.zeros(3)
        self.q_i2b_est = Quaternions([0, 0, 0, 1])
        self.q_b2b_now2tar = Quaternions([0, 0, 0, 1])
        self.q_i2b_tar = Quaternions([0, 0, 0, 1])

    def main_routine(self, count):

        self.read_sensors()

        self.determine_attitude()

        self.check_mode()

        self.calculate_control_torque()
        return

    def read_sensors(self):
        self.current_omega_c_gyro = self.components.gyro.measure(self.dynamics.attitude.current_omega_b)

    def determine_attitude(self):
        self.omega_b_est = self.current_omega_c_gyro
        att = self.dynamics.attitude.get_current_q_i2b()
        self.q_i2b_est.setquaternion(att)
        return

    def check_mode(self):

        # Vector direction of the Body frame to point to another vector
        b_dir = np.array([0, 0, 1])

        # Vector target from Inertial frame
        i_tar = np.array([1, 1, 1])
        i_tar = i_tar/np.linalg.norm(i_tar)

        # Vector target from body frame
        b_tar = self.q_i2b_est.frame_conv(i_tar)

        b_lambda = np.cross(b_dir, b_tar)
        rot = np.arcsin(np.linalg.norm(b_lambda)/(np.linalg.norm(b_tar)*np.linalg.norm(b_dir)))

        self.q_b2b_now2tar.setquaternion([b_lambda, rot])
        self.q_b2b_now2tar.normalize()
        self.q_i2b_tar = self.q_i2b_est * self.q_b2b_now2tar
        return

    def calculate_control_torque(self):
        q_b2i_est = Quaternions(self.q_i2b_est.conjugate())
        # First it is necessary to pass the quaternion from attitude to inertial,
        # then the target vector is rotated from the inertial to body frame
        q_i2b_now2tar = q_b2i_est * self.q_i2b_tar
        q_i2b_now2tar.normalize()

        torque_direction = np.zeros(3)
        torque_direction[0] = q_i2b_now2tar()[0]
        torque_direction[1] = q_i2b_now2tar()[1]
        torque_direction[2] = q_i2b_now2tar()[2]

        angle_rotation = 2*np.arccos(q_i2b_now2tar()[3])

        error_integral = self.ctrl_cycle * angle_rotation * torque_direction

        omega_b_tar = np.array([-0.0, -0.0, 0.0])
        error_omega = omega_b_tar - self.omega_b_est
        self.error_int += self.ctrl_cycle*error_omega
        self.control_torque = self.P_quat.dot(angle_rotation*torque_direction) + self.I_quat.dot(error_integral)

    def get_torque(self):
        return self.rw_torque_b

    def log_value(self):
        return

    def get_log_values(self):
        return
