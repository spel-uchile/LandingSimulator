
import numpy as np


class Thruster(object):
    def __init__(self):
        self.thruster_pos = np.array([0,0,0])
        self.thruster_dir = np.array([1, 0, 0])
        self.max_mag = 1
        self.mag_error = 0
        self.deg_error = 0
        self.id = 0
        self.thruster_b = np.array([0, 0, 0])
        self.duty = 0
        self.mag_nr = 0

    def set_duty(self, dutyratio):
        self.duty = dutyratio

    def calc_thruster(self, isReal):
        mag = self.calc_thruster_mag()
        if isReal and self.duty != 0:
            mag += self.mag_nr
        self.thruster_b = mag * self.calc_thruster_dir()
        return self.thruster_b

    def calc_thruster_mag(self):
        return 0

    def calc_thruster_dir(self):
        return

    def calc_torque(self):
        return