import numpy as np
from .SolidPropellant import SolidPropellant
from .LiquidPropellant import LiquidPropellant
from Components.Abstract.ComponentBase import ComponentBase
from .ThrusterODE import ThrusterODE

SOLID = "SOLID"
LIQUID = "LIQUID"
HYBRID = "HYBRID"
DEG2RAD = np.pi/180


class Thruster(ComponentBase, ThrusterODE):
    def __init__(self, port_id, thruster_properties):
        ComponentBase.__init__(self, 50)
        self.step_width = thruster_properties['prop_step']
        self.comp_type = thruster_properties['comp_type']
        if self.comp_type == SOLID:
            self.propellant_model = SolidPropellant(thruster_properties)
        elif self.comp_type == LIQUID:
            self.propellant_model = LiquidPropellant(thruster_properties)

        self.thruster_pos = thruster_properties['thruster_pos']
        self.thruster_dir = thruster_properties['thruster_dir']
        self.error_pos = thruster_properties['error_pos']
        self.error_dir = thruster_properties['error_dir']
        self.rotation_z = DEG2RAD*thruster_properties['rotation_z']
        self.matrix_rotation_position = np.zeros((3, 3))
        self.calc_matrix_rotation()
        # range: (0 - pi/4)
        self.ctrl_theta = 0
        self.current_torque_b = np.zeros(3)
        self.max_burn_time = 10.2
        self.current_burn_time = 0
        self.max_thrust = 10.2
        self.historical_mag_thrust = []
        self.current_thrust_i = np.zeros(3)
        self.unit_vector_control_i = np.zeros(3)
        ThrusterODE.__init__(self, self.step_width, 0.1, 2, self.max_thrust)

    def set_step_width(self, value):
        if value < self.step_width:
            self.step_width = value

    def set_thruster_ang(self, ctrl_ang):
        self.ctrl_theta = ctrl_ang

    def calc_thrust_and_torque_b(self, q_i2b):
        unit_vector_tar_b = q_i2b.frame_conv(self.unit_vector_control_i)

        unit_dir_c = np.array([- np.sin(self.ctrl_theta), 0, np.cos(self.ctrl_theta)])
        force_c = unit_dir_c * self.get_mag_thrust_c()
        self.current_thrust_b = self.matrix_rotation_position.dot(force_c)
        self.current_torque_b = np.cross(self.thruster_pos, self.current_thrust_b)

    def calc_thrust_and_torque_i(self, com_period_):
        com_period_ /= 1000
        if self.thr_is_on == 1:
            ite = 0
            while ite < com_period_ / self.step_width:
                self.update_ode()
                ite += 1
            self.current_thrust_i = self.unit_vector_control_i * self.get_mag_thrust_c()
            self.current_burn_time += self.step_width
        else:
            ite = 0
            while ite < com_period_ / self.step_width:
                self.update_ode()
                ite += 1
            self.current_thrust_i = self.unit_vector_control_i * self.get_mag_thrust_c()
            self.current_burn_time += self.step_width

    def calc_matrix_rotation(self):
        self.matrix_rotation_position[0, 0] = np.cos(self.rotation_z)
        self.matrix_rotation_position[0, 1] = -np.sin(self.rotation_z)
        self.matrix_rotation_position[1, 0] = np.sin(self.rotation_z)
        self.matrix_rotation_position[1, 1] = np.cos(self.rotation_z)

    def set_thrust_i(self, target_thrust_i):
        mag_thrust = np.linalg.norm(target_thrust_i)
        self.unit_vector_control_i = target_thrust_i / mag_thrust
        if mag_thrust < self.max_thrust:
            self.set_target_mag_thrust(mag_thrust)
        else:
            self.set_target_mag_thrust(self.max_thrust)

        if self.current_burn_time < self.max_burn_time / 2:
            self.thr_is_on = 1
        elif self.max_burn_time / 2 < self.current_burn_time <= self.max_burn_time:
            self.thr_is_on = 0
            self.set_target_mag_thrust(0)
        else:
            self.thr_is_on = 0
            self.set_target_mag_thrust(0)
            self.current_burn_time = 0

    def set_max_thrust(self, max_thrust):
        self.max_thrust = max_thrust

    def get_force_i(self):
        return self.current_thrust_i

    def get_force_b(self):
        return self.current_thrust_b

    def get_torque_b(self):
        return self.current_torque_b

    def log_value(self):
        self.historical_mag_thrust.append(self.current_mag_thrust_c)






