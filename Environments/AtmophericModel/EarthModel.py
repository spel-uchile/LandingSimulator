"""
@author: Elias Obreque

In this model is used the 1976 Standar Atmosphere
Ref:
 - https://ntrs.nasa.gov/search.jsp?R=19770009539
 - Dynamics of Atmospheric Re-entry AIAA, chapter 2
 - U.S. Standard Atmosphere 1976. Orbital Mechanics for Engineering Students
"""

import numpy as np

# Atmospheric constant
# ----------------------------------------------------------------------------------------------------------------------#
g_0 = 9.80665  # m/s2
R_atm = 287  # J/kg-K
R_gas = 8.31446261815324e3  # J/kg-mole-K
R_e = 6.381e6  # m
c2K = 273.15
Na = 6.0220978e26  # 1/g-mole
polytropic_constant = 1.405
MM0 = 28.96643  # g/mole
thermal_constant = 1.458e-6  # kg/(m-s-K**0.5) (beta)
sutherlands_constant = 110.4  # K (S)
collision_diameter = 3.65e-10  # m (sigma)
b = 3.139e-7  # 1/m
B1 = 2.64638e-3     # J/s-m-K0.5
S1 = 245.4  # K


d_0 = 1.225  # km/m^3
T_0 = 288.15  # K
P_0 = 101325  # Pa
# ----------------------------------------------------------------------------------------------------------------------#

Zi = [0, 11019, 20063.1, 32161.9, 47350.1, 51412.5, 71802.0, 86000,
      100000, 110000, 120000, 150000, 160000, 170000, 190000, 230000, 300000, 400000, 500000, 600000, 700000]
TMi = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946,
       210.65, 260.65, 360.65, 960.65, 1110.65, 1210.65, 1350.65, 1550.65, 1830.65, 2160.65, 2430.65, 2700.00]
LZi = [-6.5, 0, 1, 2.8, 0, -2.8, -2.0, 1.6481, 5, 10, 20, 15, 10, 7, 5, 4, 3.3, 2.6, 1.7, 1.1]
MMi = [28.96643, 28.96643, 28.96643, 28.96643, 28.96643, 28.96643, 28.96643, 28.9644, 28.88,
       28.56, 28.08, 26.92, 26.66, 26.49, 25.85, 24.70, 22.65, 19.94, 16.84, 16.17]
flag = {'atm_calculation': True}


class EarthModel(object):
    def __init__(self, properties=flag):
        self.envir_flag = properties['atm_calculation']
        self.envir_logging = properties['atm_logging']
        # State
        self.density = d_0  # kg/m3
        self.air_temperature = T_0  # K: Air Temperature
        self.molecular_temperature = T_0  # K: Molecular temperature
        self.pressure = P_0  # Pa
        self.base_pressure = P_0
        self.base_density = d_0
        self.flag_base = True
        self.Lz = 0
        self.Na = Na
        self.gamma = 1.4
        self.R_atm = R_atm  # J/ kgK
        self.sonic_speed = 340
        self.part_speed = 340
        self.MM = MM0
        self.collision_freq = 0.2
        self.path_length = 0.1
        self.dynamics_viscosity = 0.1
        self.kinematic_viscosity = 0.1
        self.kt = 0.1
        self.boltzmann = 1.3806488e-23  # J/K
        self.historical_pressure = []
        self.historical_temperature = []
        self.historical_density = []

    def update(self, dynamics, decyear):
        self.calc_atmospferic_data(dynamics.trajectory.current_alt)

    def save_data(self):
        self.historical_density.append(self.density)
        self.historical_pressure.append(self.pressure)
        self.historical_temperature.append(self.molecular_temperature)

    def _calc_atmospheric_quantities(self):
        # Speed of sound
        self.sonic_speed = np.sqrt(self.gamma * self.R_atm * self.air_temperature)  # m/s
        # Air particle speed
        self.part_speed = np.sqrt((8.0 * self.R_atm * self.molecular_temperature / np.pi))
        # Collision frequency
        self.collision_freq = np.sqrt(2) * np.pi * collision_diameter ** 2 * self.part_speed * Na
        # Mean Free path length
        self.path_length = self.part_speed / self.collision_freq
        # viscocity
        self.dynamics_viscosity = thermal_constant * self.molecular_temperature ** (3 / 2) / \
                                  (self.molecular_temperature + sutherlands_constant)
        self.kinematic_viscosity = self.dynamics_viscosity / self.density
        # Thermal conductivity J/smK
        self.kt = B1 * self.molecular_temperature ** (3 / 2) / \
                 (self.molecular_temperature + S1 * (10 ** (-12 / self.molecular_temperature)))

    def calc_atmospferic_data(self, altitude):
        pressure    = []
        density     = []
        temperature = []
        MassMol     = []
        if type(altitude) == float or type(altitude) == int or altitude.size == 1:
            Z = [altitude]
        else:
            Z = altitude
        for z in Z:
            Pi = P_0
            deni = d_0
            mmi = MM0
            for i in range(len(Zi)-1):
                if z <= Zi[i + 1]:
                    if LZi[i] == 0:
                        pres, den, temp = self._calc_state_at_zeroISA(z, Zi[i], Pi, TMi[i], deni)
                        temperature.append(temp)
                        pressure.append(pres)
                        density.append(den)
                        MassMol.append(mmi + (MMi[i] - mmi)/(Zi[i + 1] - Zi[i]) * (z - Zi[i]))
                    else:
                        pres, den, temp = self._calc_state_not_zeroISA(z, Zi[i], Pi, TMi[i], deni, LZi[i])
                        temperature.append(temp)
                        pressure.append(pres)
                        density.append(den)
                        MassMol.append(mmi + (MMi[i] - mmi)/(Zi[i + 1] - Zi[i]) * (z - Zi[i]))
                    break
                else:
                    if LZi[i] == 0:
                        Pi, deni, _ = self._calc_state_at_zeroISA(Zi[i + 1], Zi[i], Pi, TMi[i], deni)
                        mmi = MMi[i]
                    else:
                        Pi, deni, _ = self._calc_state_not_zeroISA(Zi[i + 1], Zi[i], Pi, TMi[i], deni, LZi[i])
                        mmi = MMi[i]
        self.air_temperature = np.array(temperature)
        self.pressure = np.array(pressure)
        self.density = np.array(density)
        self.MM = np.array(MassMol)
        self.molecular_temperature = self.MM * self.air_temperature / MM0
        self._calc_atmospheric_quantities()

    @staticmethod
    def _calc_state_at_zeroISA(z, zi, Pi, tmi, deni):
        p1 = Pi * np.exp(-g_0 / R_atm / tmi * (z - zi))
        den = p1 / (R_atm * tmi)
        return p1, den, tmi

    @staticmethod
    def _calc_state_not_zeroISA(z, zi, Pi, tmi, deni, L):
        L *= 0.001
        t1 = tmi + L * (z - zi)
        p1 = Pi * (t1 / tmi) ** (-g_0 / L / R_atm)
        den = p1 / (R_atm * t1)
        return p1, den, t1

    def create_report(self):
        report_atm = {'Pressure [Pa]': np.array(self.historical_pressure)[:,0],
                      'Temperature [K]': np.array(self.historical_temperature)[:,0],
                      'Density [kg/m^3]': np.array(self.historical_density)[:,0]}
        return report_atm


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    atm = EarthModel(flag)
    H = np.linspace(0, 80000, 100)
    atm.calc_atmospferic_data(165000)

    if len(atm.pressure) > 1:
        plt.figure()
        plt.grid()
        plt.title('Pressure [Pa]')
        plt.plot(H, atm.pressure)
        plt.show()

        plt.figure()
        plt.grid()
        plt.title('Density [kg/m3]')
        plt.plot(H, atm.density)
        plt.show()

        plt.figure()
        plt.grid()
        plt.title('Temperature [K]')
        plt.plot(H, atm.molecular_temperature)
        plt.show()

        plt.figure()
        plt.grid()
        plt.title('Sonic Speed [m/s]')
        plt.plot(H, atm.sonic_speed)
        plt.show()

        plt.figure()
        plt.grid()
        plt.title('Dynamics viscosity [Pa.s]')
        plt.plot(H, atm.dynamics_viscosity)
        plt.show()

        plt.figure()
        plt.grid()
        plt.title('Kinematic viscosity [m2/s]')
        plt.plot(H, atm.kinematic_viscosity)
        plt.show()
    else:
        print('Pressure: ', atm.pressure, ' [Pa]')
        print('Temperature: ', atm.molecular_temperature, ' [K]')
        print('Density: ', atm.density, ' [kg/m3]')
        print('Sonic spees: ', atm.sonic_speed, ' [m/s]')
        print('Dynamic viscosity: ', atm.dynamics_viscosity, ' [Pa.s]')
        print('Molar mass: ', atm.MM, ' [g/mol]')





