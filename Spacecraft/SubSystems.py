
from Interface.InitSubsystems.InitSubSystems import InitSubSystems
from Components.Abstract.ADCS import ADCS
from Components.Abstract.ODCS import ODCS
import numpy as np


class SubSystems(InitSubSystems):
    def __init__(self, components_properties, dynamics, prop_step):
        InitSubSystems.__init__(self, components_properties,  prop_step)

        cdh = None
        adcs = ADCS(self.init_components['ADCS'], self.system_init_setting['ADCS'], dynamics)
        odcs = ODCS(self.init_components['ODCS'], dynamics)
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
        return self.subsystems['ADCS'].get_torque() + self.subsystems['ODCS'].get_torque()

    def generate_force_b(self):
        return self.subsystems['ODCS'].get_force()

    def save_log_values(self):
        for sub_elem in self.system_name:
            if self.subsystems[sub_elem] is not None:
                for comp in self.subsystems[sub_elem].components.get_list:
                    if comp is not None:
                        comp.log_value()