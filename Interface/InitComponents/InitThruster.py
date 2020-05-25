"""
Created: 4/13/2020
Autor: Elias Obreque Sepulveda
email: els.obrq@gmail.com

"""
import configparser
import numpy as np


class InitThruster(object):
    def __init__(self, path_com, prop_step):
        config_com = configparser.ConfigParser()
        directory = path_com + 'Thruster.ini'
        config_com.read(directory, encoding="utf8")
        number_thruster = int(config_com['SETTING']['number_thruster'])
        self.thruster_properties = []
        for i in range(1, number_thruster + 1):
            thruster_n = 'Thruster' + str(i)
            thruster_pos = np.zeros(3)
            thruster_pos[0] = config_com[thruster_n]['thruster_pos(0)']
            thruster_pos[1] = config_com[thruster_n]['thruster_pos(1)']
            thruster_pos[2] = config_com[thruster_n]['thruster_pos(2)']

            thruster_dir = np.zeros(3)
            thruster_dir[0] = config_com[thruster_n]['thruster_dir(0)']
            thruster_dir[1] = config_com[thruster_n]['thruster_dir(1)']
            thruster_dir[2] = config_com[thruster_n]['thruster_dir(2)']

            thruster_properties = {'comp_type': config_com[thruster_n]['comp_type'],
                                   'burn_area': config_com[thruster_n]['burn_area'],
                                   'diameter_ext': float(config_com[thruster_n]['diameter_ext']),
                                   'diameter_int': float(config_com[thruster_n]['diameter_int']),
                                   'large': float(config_com[thruster_n]['large']),
                                   'number_point': float(config_com[thruster_n]['number_point']),
                                   'burn_rate': float(config_com[thruster_n]['burn_rate']),
                                   'thruster_pos': thruster_pos,
                                   'error_pos': float(config_com[thruster_n]['error_pos']),
                                   'thruster_dir': thruster_dir,
                                   'error_dir': float(config_com[thruster_n]['error_dir']),
                                   'MassMolar': float(config_com[thruster_n]['MM']),
                                   'density_p': float(config_com[thruster_n]['density_p']),
                                   'rotation_z': float(config_com[thruster_n]['rotation_z']),
                                   'prop_step': prop_step}
            self.thruster_properties.append(thruster_properties)
