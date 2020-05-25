
import numpy as np
from Library.igrf.IGRF import calculate_igrf
from Library.math_sup.tools_reference_frame import rotationY, rotationZ

RAD2DEG = 180/np.pi
DEG2RAD = 1/RAD2DEG


class MagEnv(object):
    def __init__(self, mag_properties):
        self.envir_flag = mag_properties['mag_calculation']
        self.envir_logging = mag_properties['mag_logging']
        self.Mag_i = np.zeros(3)
        self.Mag_b = np.zeros(3)
        self.historical_mag_b = []
        self.historical_mag_i = []
        self.calcmagflag = True

    def update(self, dynamics, decyear):
        sideral = dynamics.ephemeris.selected_center_object.current_sideral
        lat = dynamics.trajectory.current_lat
        lon = dynamics.trajectory.current_long
        alt = dynamics.trajectory.current_alt
        q_i2b = dynamics.attitude.current_quaternion_i2b
        self.calc_mag(decyear, sideral, lat, lon, alt, q_i2b)

    def save_data(self):
        self.historical_mag_b.append(self.Mag_b)
        self.historical_mag_i.append(self.Mag_i)

    def calc_mag(self, decyear, sideral, lat, lon, alt, q_i2b):
        if not self.calcmagflag:
            return
        alt /= 1000
        """
         itype = 1 if geodetic(spheroid)
         itype = 2 if geocentric(sphere)
         alt   = height in km above sea level if itype = 1
               = distance from centre of Earth in km if itype = 2 (>3485 km)
        """
        x, y, z, f, gccolat = calculate_igrf(0, decyear, alt, lat, lon, itype=1)
        mag_local = [x, y, z]

        self._mag_NED_to_ECI(mag_local, gccolat, lon, sideral)

        self.Mag_b = q_i2b.frame_conv(self.Mag_i)

    def add_mag_noise(self):
        return

    def _mag_NED_to_ECI(self, mag_0, theta, lonrad, gmst):
        mag_local_0y = rotationY(mag_0, np.pi - theta)
        mag_local_yz = rotationZ(mag_local_0y, -lonrad)
        self.Mag_i   = rotationZ(mag_local_yz, -gmst)

    def get_mag_b(self):
        return self.Mag_b

    def create_report(self):
        report_mag = {'Mag_b_X [Nm]': np.array(self.historical_mag_b)[:, 0],
                      'Mag_b_Y [Nm]': np.array(self.historical_mag_b)[:, 1],
                      'Mag_b_Z [Nm]': np.array(self.historical_mag_b)[:, 2],
                      'Mag_i_X [Nm]': np.array(self.historical_mag_i)[:, 0],
                      'Mag_i_Y [Nm]': np.array(self.historical_mag_i)[:, 1],
                      'Mag_i_Z [Nm]': np.array(self.historical_mag_i)[:, 2]}
        return report_mag
