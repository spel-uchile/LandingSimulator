
import numpy as np
from .AirDrag import AirDrag
from .GravGrad import GravGrad


class Disturbances(object):
    def __init__(self, disturbance_properties, environment, spacecraft):
        self.dist_environment = environment
        self.dist_spacecraft = spacecraft
        self.disturbance_ = []
        if disturbance_properties['GRA']['gra_calculation']:
            grav = GravGrad(disturbance_properties['GRA'], self.dist_spacecraft)
            self.disturbance_.append(grav)
        if disturbance_properties['ADRAG']['atm_calculation']:
            atmd = AirDrag(disturbance_properties['ADRAG'], disturbance_properties['SFF'])
            self.disturbance_.append(atmd)

        self.dist_torque_b = np.zeros(3)
        self.dist_force_b  = np.zeros(3)

    def update(self):
        self.reset_output()

        for dist in self.disturbance_:
            if dist.dist_flag:
                dist.update(self.dist_environment, self.dist_spacecraft)
                self.dist_torque_b += dist.get_torque_b()
                self.dist_force_b += dist.get_force_b()

    def create_report(self):
        report_dist = {}
        for dist in self.disturbance_:
            if dist.dist_logging:
                report_dist = {**report_dist,
                               **dist.create_report()}
        return report_dist

    def update_data(self):
        for dist in self.disturbance_:
            if dist.dist_logging:
                dist.save_data()

    def get_dist_torque_b(self):
        return self.dist_torque_b

    def get_dis_force_b(self):
        return self.dist_force_b

    def reset_output(self):
        self.dist_torque_b = np.zeros(3)
        self.dist_force_b  = np.zeros(3)
