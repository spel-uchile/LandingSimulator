
from Interface.InitSubsystems.InitSubSystems import InitSubSystems
from Components.Abstract.ADCS import ADCS
from Components.Abstract.ODCS import ODCS
import numpy as np


class SubSystems(InitSubSystems):
    def __init__(self, components_properties, dynamics, prop_step):
        InitSubSystems.__init__(self, components_properties,  prop_step)

        if components_properties['create_cdh']:
            cdh = None
        else:
            cdh = None
        if components_properties['create_adcs']:
            adcs = ADCS(self.init_components['ADCS'], self.system_init_setting['ADCS'], dynamics)
        else:
            adcs = None
        if components_properties['create_odcs']:
            odcs = ODCS(self.init_components['ODCS'], self.system_init_setting['ODCS'], dynamics)
        else:
            odcs = None
        power = None
        com = None
        str = None
        payload = None
        tcs = None

        self.subsystems = {'CDH': cdh,
                           'ADCS': adcs,
                           'ODCS': odcs,
                           'POWER': power,
                           'COM': com,
                           'STR': str,
                           'PAYLOAD': payload,
                           'TCS': tcs}

    def generate_torque_b(self):
        return self.subsystems['ODCS'].get_torque_b()

    def generate_force_b(self):
        return self.subsystems['ODCS'].get_force_b()

    def generate_force_i(self):
        return self.subsystems['ODCS'].get_force_i()

    def save_log_values(self):
        for sub_elem in self.system_name:
            if self.subsystems[sub_elem] is not None:
                self.subsystems[sub_elem].log_value()
                for comp in self.subsystems[sub_elem].components.get_list:
                    if comp is not None:
                        comp.log_value()