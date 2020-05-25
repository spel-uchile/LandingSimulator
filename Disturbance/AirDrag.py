
"""
Created by:

@author: Elias Obreque
els.obrq@gmail.com

ref to force and torque definition:
 - Dynamics of Atmospheric Re-entry AIAA, chapter 11, eq. (11.24)
 - Gauss error function
 - Generic Computation Method of Free-Molecular Flow Effects on Space Objects,  By Takahiro KATO
"""
from scipy.special import erf
import numpy as np
from .SurfaceForce import SurfaceForce
c2K = 273.15

FREE_MOLECULAR = 'FREE_MOLECULAR'
TRANSITION = 'TRANSITION'
CONTINUUM_FLOW = 'CONTINUUM_FLOW'


class AirDrag(SurfaceForce):
    def __init__(self, drag_properties, surface_properties):
        SurfaceForce.__init__(self, surface_properties)
        self.dist_flag = drag_properties['atm_calculation']
        self.dist_logging = drag_properties['atm_logging']
        self.module_wall_temperature = drag_properties['Temp_wall'] + c2K
        self.specularity = drag_properties['specularity']
        self.reflectivity = np.ones(6)
        self.Kn = 10
        self.Cp = 0.1
        self.Ct = 0.1
        self.char_dimension = 0.1
        self.regimen_set = None
        self.sigma_n = 1 - self.specularity
        self.sigma_t = self.sigma_n
        self.historical_force_b = []
        self.historical_torque_b = []

    def update(self, environment, spacecraft):
        density = environment.atm.density
        velocity_b = spacecraft.dynamics.trajectory.get_velocity_b()
        velocity_b_norm = np.linalg.norm(velocity_b)
        q_inf = 0.5 * density * velocity_b_norm ** 2
        self.calc_knudsen_number(environment, np.max(abs(self.position_vector_face)), velocity_b_norm)
        self.set_regimen_flow()
        unit_velocity_b = velocity_b / velocity_b_norm
        self.calc_ang_parameters(unit_velocity_b)
        self.calc_aerodynamics_coeff(environment, velocity_b_norm)
        self.calc_force_torque_vector_b(unit_velocity_b, self.Cp, self.Ct)

    def get_torque_b(self):
        return self.torque_vector_b

    def get_force_b(self):
        return self.force_vector_b

    def calc_aerodynamics_coeff(self, envir, v_b):
        if self.regimen_set == FREE_MOLECULAR:
            s = np.sqrt((envir.atm.MM * v_b ** 2) / (2 * envir.atm.boltzmann * self.module_wall_temperature))
            ss = s ** 2
            sn = s * self.cos_theta[self.condition_]
            st = s * self.sen_theta[self.condition_]
            s2sn = 2 - self.sigma_n[self.condition_]
            sntw_tinf = 0.5 * self.sigma_n[self.condition_] * (self.module_wall_temperature /
                                                               envir.atm.molecular_temperature) ** 0.5
            erf_c_theta = 1 + erf(sn)
            sqrt_pi = np.sqrt(np.pi)
            sn2 = sn ** 2
            exp_sn = np.exp(- sn2)
            gt_sn_pi = self.sigma_t[self.condition_] * st / sqrt_pi
            deltaP_q_inf_s2 = [s2sn * sn / sqrt_pi + sntw_tinf] * exp_sn + \
                              [s2sn * (0.5 + sn2) + sntw_tinf * sqrt_pi * sn] * erf_c_theta
            deltaT_q_inf_s2 = gt_sn_pi * (exp_sn + sqrt_pi * sn * erf_c_theta)
            self.Cp = deltaP_q_inf_s2 / ss
            self.Ct = deltaT_q_inf_s2 / ss
        elif self.regimen_set == TRANSITION:
            self.Cp = 0.1
            self.Ct = 0.1
        elif self.regimen_set == CONTINUUM_FLOW:
            # For Newtonian Pressure
            # s = M * sqrt(gamma(2)  = V_b/v_m  and s is very large
            # sigma_n = 1.0, sigma_t = 0.0
            # TW/Tinf = 0.0
            self.sigma_n = np.ones(6)
            self.sigma_t = np.zeros(6)
            s = np.sqrt((envir.atm.MM * v_b ** 2) / (2 * envir.atm.boltzmann * self.module_wall_temperature))
            ss = s ** 2
            sn = s * self.cos_theta[self.condition_]
            st = s * self.sen_theta[self.condition_]
            s2sn = 2 - self.sigma_n[self.condition_]
            sntw_tinf = 0.5 * self.sigma_n[self.condition_] * 0
            erf_c_theta = 1 + erf(sn)
            sqrt_pi = np.sqrt(np.pi)
            sn2 = sn ** 2
            exp_sn = np.exp(- sn2)
            gt_sn_pi = self.sigma_t[self.condition_] * st / sqrt_pi
            deltaP_q_inf_s2 = [s2sn * sn / sqrt_pi + sntw_tinf] * exp_sn + \
                              [s2sn * (0.5 + sn2) + sntw_tinf * sqrt_pi * sn] * erf_c_theta
            deltaT_q_inf_s2 = gt_sn_pi * (exp_sn + sqrt_pi * sn * erf_c_theta)
            self.Cp = deltaP_q_inf_s2 / ss
            self.Ct = deltaT_q_inf_s2 / ss
        else:
            print('No regimen flow set')

    def set_regimen_flow(self):
        if self.Kn >= 10:
            self.regimen_set = FREE_MOLECULAR
        elif 0.01 < self.Kn < 10:
            self.regimen_set = TRANSITION
        else:
            self.regimen_set = CONTINUUM_FLOW

    def calc_knudsen_number(self, envir, L, velocity_b_norm):
        """
         A high Kn indicates the importance of the particulate nature of the fluid and that the Boltzmann equation
         must be employed, whereas a low Kn permits treatment of the fluid as a continuum and the use of the
         Navier-Stokes equations

        gamma_inf: is a corrected mean free path that accounts fot the state of particles emitted from the body
        """
        M_inf = velocity_b_norm / envir.atm.sonic_speed
        print(M_inf, envir.atm.pressure)
        gamma_inf = 4/np.sqrt(np.pi * envir.atm.gamma) * (self.module_wall_temperature / envir.atm.molecular_temperature) ** 0.5 *\
                    (envir.atm.path_length / M_inf)
        self.Kn = gamma_inf / L

    def save_data(self):
        self.historical_force_b.append(self.force_vector_b)
        self.historical_torque_b.append(self.torque_vector_b)

    def create_report(self):
        report = {'Drag_force_b_X [N]': np.array(self.historical_force_b)[:, 0],
                  'Drag_force_b_Y [N]': np.array(self.historical_force_b)[:, 1],
                  'Drag_force_b_Z [N]': np.array(self.historical_force_b)[:, 2],
                  'Drag_torque_b_X [Nm]': np.array(self.historical_torque_b)[:, 0],
                  'Drag_torque_b_Y [Nm]': np.array(self.historical_torque_b)[:, 1],
                  'Drag_torque_b_Z [Nm]': np.array(self.historical_torque_b)[:, 2]}
        return report
