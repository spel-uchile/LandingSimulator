
import configparser
import numpy as np


class InitADCS(object):
    def __init__(self, file_path):

        section = 'SETTING'
        config = configparser.ConfigParser()
        config.read(file_path, encoding="utf8")

        q_b2c = np.zeros(4)
        q_b2c[0] = config[section]['q_b2c(0)']
        q_b2c[1] = config[section]['q_b2c(1)']
        q_b2c[2] = config[section]['q_b2c(2)']
        q_b2c[3] = config[section]['q_b2c(3)']

        P_quat = np.diag([1.0, 1.0, 1.0])
        P_quat[0, 0] = config[section]['P_quat(0)']
        P_quat[1, 1] = config[section]['P_quat(1)']
        P_quat[2, 2] = config[section]['P_quat(2)']

        I_quat = np.diag([1.0, 1.0, 1.0])
        I_quat[0, 0] = config[section]['I_quat(0)']
        I_quat[1, 1] = config[section]['I_quat(1)']
        I_quat[2, 2] = config[section]['I_quat(2)']

        P_omega = np.diag([1.0, 1.0, 1.0])
        P_omega[0, 0] = config[section]['P_omega(0)']
        P_omega[1, 1] = config[section]['P_omega(1)']
        P_omega[2, 2] = config[section]['P_omega(2)']

        self.properties_ = {'port_id': float(config[section]['port_id']),
                            'ADCS_COMPONENT_NUMBER': float(config[section]['ADCS_COMPONENT_NUMBER']),
                            'ADCS_com_frequency': float(config[section]['ADCS_com_frequency']),
                            'q_b2c': q_b2c,
                            'P_quat': P_quat,
                            'I_quat': I_quat,
                            'P_omega': P_omega}

    def get_setting(self):
        return self.properties_

