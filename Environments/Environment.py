
from .MagEnv import MagEnv
from .AtmophericModel.EarthModel import EarthModel


class Environment(object):
    def __init__(self, environment_properties):
        self.envir = []
        print('\nEnvironment properties')
        print('------------------------------')
        self.atm = None
        self.magnetic = None
        if environment_properties['ATM']['atm_calculation']:
            self.atm = EarthModel(environment_properties['ATM'])
            self.envir.append(self.atm)
            print('Atmosphere: ' + str(self.atm.envir_flag))
        if environment_properties['MAG']['mag_calculation']:
            self.magnetic = MagEnv(environment_properties['MAG'])
            self.envir.append(self.magnetic)
            print('Magnetic: ' + str(self.magnetic.envir_flag))
        print('------------------------------')

    def update(self, decyear, dynamics):
        for env in self.envir:
            if env.envir_flag:
                env.update(dynamics, decyear)

    def update_data(self):
        for env in self.envir:
            if env.envir_logging:
                env.save_data()

    def create_report(self):
        report_envir = {}
        for env in self.envir:
            if env.envir_logging:
                report_envir = {**report_envir,
                                **env.create_report()}
        return report_envir
