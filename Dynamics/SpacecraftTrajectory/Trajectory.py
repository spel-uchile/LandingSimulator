# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 03:00:38 2020

@author: EO
"""

import numpy as np
from .TwoBodyProblem import TwoBodyProblem
from Library.math_sup.tools_reference_frame import fmod2

twopi = 2.0 * np.pi
deg2rad = np.pi / 180.0
rad2deg = 1 / deg2rad


class Trajectory(object):
    def __init__(self, spacecraft_trajectory, step_width, selected_planet):
        self.step_width             = step_width
        self.trajectory_properties  = spacecraft_trajectory['Orbit_info']
        self.propagation_model      = spacecraft_trajectory['propagate']
        self.reference_frame        = spacecraft_trajectory['reference_frame']
        self.current_position       = self.trajectory_properties[0]
        self.current_velocity       = self.trajectory_properties[1]
        self.current_long           = 0
        self.current_lat            = 0
        self.current_alt            = 0
        self.historical_position_i  = []
        self.historical_velocity_i  = []
        self.historical_lats        = []
        self.historical_longs       = []
        self.historical_alts        = []
        self.selected_propagator    = None
        self.selected_planet        = selected_planet
        self.force_i                = np.zeros(3)

    def set_propagator(self):
        if self.propagation_model == 0:
            if self.reference_frame == 1:
                self.selected_propagator = TwoBodyProblem(self.selected_planet.mu,
                                                          self.step_width,
                                                          self.current_position,
                                                          self.current_velocity)
            elif self.reference_frame == 2:
                geodetic_long = self.current_position[0]
                geodetic_lat = self.current_position[1]
                geodetic_alt = self.current_position[2]
        elif self.propagation_model == 1:
            self.selected_propagator = 0

    def update(self, array_time):
        self.current_position, self.current_velocity = self.selected_propagator.update_state(array_time)

    def add_force_b(self, force_i):
        self.force_i += force_i
        self.selected_propagator.set_acc_i(self.force_i)

    def get_ext_force_b(self):
        return self.force_i

    def TransECItoGeo(self, current_sideral):
        r = np.sqrt(self.current_position[0] ** 2 + self.current_position[1] ** 2)

        long = fmod2(np.arctan2(self.current_position[1], self.current_position[0]) - current_sideral)
        lat = np.arctan2(self.current_position[2], r)

        flag_iteration = True

        while flag_iteration:
            phi = lat
            c = 1 / np.sqrt(1 - self.selected_planet.e2 * np.sin(phi) * np.sin(phi))
            lat = np.arctan2(self.current_position[2] + self.selected_planet.radiuskm * c
                             * self.selected_planet.e2 * np.sin(phi) * 1000, r)
            if (np.abs(lat - phi)) <= self.selected_planet.tolerance:
                flag_iteration = False

        alt = r / np.cos(lat) - self.selected_planet.radiuskm * c * 1000  # *metros
        if lat > np.pi / 2:
            lat -= twopi
        self.current_alt = alt
        self.current_lat = lat
        self.current_long = long
        return lat, long, alt

    def save_orbit_data(self):
        self.historical_position_i.append(self.current_position)
        self.historical_velocity_i.append(self.current_velocity)
        self.historical_lats.append(self.current_lat)
        self.historical_longs.append(self.current_long)
        self.historical_alts.append(self.current_alt)

    def get_log_values(self):
        report_orbit = {'sat_position_i(X)[m]': np.array(self.historical_position_i)[:, 0],
                        'sat_position_i(Y)[m]': np.array(self.historical_position_i)[:, 1],
                        'sat_position_i(Z)[m]': np.array(self.historical_position_i)[:, 2],
                        'sat_velocity_i(X)[m/s]': np.array(self.historical_velocity_i)[:, 0],
                        'sat_velocity_i(Y)[m/s]': np.array(self.historical_velocity_i)[:, 1],
                        'sat_velocity_i(Z)[m/s]': np.array(self.historical_velocity_i)[:, 2],
                        'lat[rad]': np.array(self.historical_lats),
                        'lon[rad]': np.array(self.historical_longs),
                        'alt[m]': np.array(self.historical_alts)}
        return report_orbit

