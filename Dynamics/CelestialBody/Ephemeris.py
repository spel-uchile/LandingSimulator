# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:52:52 2019

@author: Elias
"""
from .Earth import Earth
from .Mars import Mars
from .Moon import Moon


class Ephemeris(object):
    def __init__(self, ephemerides_properties):
        self.inertial_frame = ephemerides_properties['inertial_frame']
        self.aberration_correction = ephemerides_properties['aberration_correction']
        self.center_object = ephemerides_properties['center_object']
        self.num_of_selected_body = ephemerides_properties['num_of_selected_body']

        if self.center_object == 'EARTH':
            self.selected_center_object = Earth()
        elif self.center_object == 'MOON':
            self.selected_center_object = Moon()
        elif self.center_object == 'MARS':
            self.center_object = Mars()
        else:
            print('Central object not selected')

    def update(self, current_jd):
        self.selected_center_object.update_state(current_jd)

    def save_ephemeris_data(self):
        self.selected_center_object.save_data()



