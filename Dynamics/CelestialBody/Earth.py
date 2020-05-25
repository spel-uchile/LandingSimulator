
import numpy as np
from Library.math_sup.tools_reference_frame import gstime

twopi       = 2.0 * np.pi
deg2rad     = np.pi / 180.0


class Earth(object):
    def __init__(self, wgs=2):
        self.historical_gst = []
        self.h_gst = {}
        self.current_sideral = 0
        if wgs == 0:
            #  ------------ wgs-72 old constants ------------
            self.radiuskm = 6378.135  # km
            self.mu = 3.9860079964e14  # in m3 / s2
            self.radiuskm = 6378.135  # km
            self.xke = 0.0743669161
            self.tumin = 1.0 / self.xke
            self.j2 = 0.001082616
            self.j3 = -0.00000253881
            self.j4 = -0.00000165597
            self.j3oj2 = self.j3 / self.j2
            self.f = 1.0 / 298.26
        elif wgs == 1:
            #  ------------ wgs-72 constants ------------
            self.radiuskm = 6378.135  # km
            self.mu = 3.986008e14  # in m3 / s2
            self.radiuskm = 6378.135  # km
            self.xke = 60.0 / np.sqrt(self.radiuskm * self.radiuskm * self.radiuskm / self.mu)
            self.tumin = 1.0 / self.xke
            self.j2 = 0.001082616
            self.j3 = -0.00000253881
            self.j4 = -0.00000165597
            self.j3oj2 = self.j3 / self.j2
            self.f = 1.0 / 298.26
        elif wgs == 2:
            #  ------------ wgs-84 constants ------------
            self.radiuskm = 6378.137  # km
            self.mu = 3.986005e14  # in m3 / s2
            self.xke = 60.0 / np.sqrt(self.radiuskm * self.radiuskm * self.radiuskm / self.mu)
            self.tumin = 1.0 / self.xke
            self.j2 = 0.00108262998905
            self.j3 = -0.00000253215306
            self.j4 = -0.00000161098761
            self.j3oj2 = self.j3 / self.j2
            self.f = 1.0 / 298.257223563
        else:
            print('wgs not used')
        self.e2 = self.f * (2 - self.f)
        self.tolerance = 1e-10  # rad

    def save_data(self):
        self.historical_gst.append(self.current_sideral)

    def update_state(self, current_jd):
        self.current_sideral = gstime(current_jd)

    def get_current_sideral(self):
        return self.current_sideral

    def get_log_values(self):
        h_gst = {'GST [rad]': self.historical_gst}
        return h_gst
