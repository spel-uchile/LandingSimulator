"""
Created: 4/8/2020
Autor: Elias Obreque Sepulveda
email: els.obrq@gmail.com

"""
import numpy as np

STAR = 'STAR'
TUBULAR = 'TUBULAR'
ENDBURN = 'ENDBURN'


class SolidPropellant(object):
    def __init__(self, properties):
        self.propellant_grain_type = properties['burn_area']
        self.diameter_ext = properties['diameter_ext']
        self.diameter_int = properties['diameter_int']

        if self.propellant_grain_type == STAR:
            self.star_propellant()
        elif self.propellant_grain_type == TUBULAR:
            self.tubular_propellant()
        elif self.propellant_grain_type == ENDBURN:
            self.endburn_propellant()
        else:
            print('No selected propellant grain type')

    def star_propellant(self):
        return

    def tubular_propellant(self):


        return

    def endburn_propellant(self):
        return