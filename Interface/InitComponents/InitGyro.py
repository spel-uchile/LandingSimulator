
import configparser
import numpy as np


class InitGyro(object):
    def __init__(self, path_com):
        config_com = configparser.ConfigParser()
        directory = path_com + 'gyro.ini'

        config_com.read(directory, encoding="utf8")

        q_b2c = np.zeros(4)
        q_b2c[0] = config_com['GYRO']['q_b2c(0)']
        q_b2c[1] = config_com['GYRO']['q_b2c(1)']
        q_b2c[2] = config_com['GYRO']['q_b2c(2)']
        q_b2c[3] = config_com['GYRO']['q_b2c(3)']

        ScaleFactor = np.zeros((3, 3))
        ScaleFactor[0, 0] = config_com['GYRO']['ScaleFactor(0)']
        ScaleFactor[0, 1] = config_com['GYRO']['ScaleFactor(1)']
        ScaleFactor[0, 2] = config_com['GYRO']['ScaleFactor(2)']
        ScaleFactor[1, 0] = config_com['GYRO']['ScaleFactor(3)']
        ScaleFactor[1, 1] = config_com['GYRO']['ScaleFactor(4)']
        ScaleFactor[1, 2] = config_com['GYRO']['ScaleFactor(5)']
        ScaleFactor[2, 0] = config_com['GYRO']['ScaleFactor(6)']
        ScaleFactor[2, 1] = config_com['GYRO']['ScaleFactor(7)']
        ScaleFactor[2, 2] = config_com['GYRO']['ScaleFactor(8)']

        Bias_c = np.zeros(3)
        Bias_c[0] = config_com['GYRO']['Bias_c(0)']
        Bias_c[1] = config_com['GYRO']['Bias_c(1)']
        Bias_c[2] = config_com['GYRO']['Bias_c(2)']

        rw_stepwidth = float(config_com['GYRO']['rw_stepwidth'])

        rw_stddev_c = np.zeros(3)
        rw_stddev_c[0] = config_com['GYRO']['rw_stddev_c(0)']
        rw_stddev_c[1] = config_com['GYRO']['rw_stddev_c(1)']
        rw_stddev_c[2] = config_com['GYRO']['rw_stddev_c(2)']

        rw_limit_c = np.zeros(3)
        rw_limit_c[0] = config_com['GYRO']['rw_limit_c(0)']
        rw_limit_c[1] = config_com['GYRO']['rw_limit_c(1)']
        rw_limit_c[2] = config_com['GYRO']['rw_limit_c(2)']

        nr_stddev_c = np.zeros(3)
        nr_stddev_c[0] = config_com['GYRO']['nr_stddev_c(0)']
        nr_stddev_c[1] = config_com['GYRO']['nr_stddev_c(1)']
        nr_stddev_c[2] = config_com['GYRO']['nr_stddev_c(2)']

        Range_to_const = float(config_com['GYRO']['Range_to_const'])
        Range_to_zero = float(config_com['GYRO']['Range_to_zero'])

        current = float(config_com['GYRO']['current'])

        self.gyro_properties = {'q_b2c': q_b2c,
                                'ScaleFactor': ScaleFactor,
                                'Bias_c': Bias_c,
                                'rw_stepwidth': rw_stepwidth,
                                'rw_stddev_c': rw_stddev_c,
                                'rw_limit_c': rw_limit_c,
                                'nr_stddev_c': nr_stddev_c,
                                'Range_to_const': Range_to_const,
                                'Range_to_zero': Range_to_zero,
                                'current': current}
        print(' - Gyro added')
