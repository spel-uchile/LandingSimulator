
import numpy as np
from .AirDrag import AirDrag
from .GravGrad import GravGrad


class Disturbances(object):
    def __init__(self, disturbance_properties, environment, spacecraft):
        grav = GravGrad(disturbance_properties['GRA'])
        self.dist_environment = environment
        self.dist_spacecraft = spacecraft

        self.disturbance_ = [grav]

        self.dist_torque_b = np.zeros(3)
        self.dist_force_b  = np.zeros(3)

    def update(self):
        self.reset_output()

        for dist in self.disturbance_:
            if dist.dist_flag:
                dist.update(self.dist_environment, self.dist_spacecraft)
                self.dist_torque_b += dist.get_torque_b()

    def get_dist_torque(self):
        return self.dist_torque_b

    def get_dis_force(self):
        return self.dist_force_b

    def reset_output(self):
        self.dist_torque_b = np.zeros(3)
        self.dist_force_b  = np.zeros(3)
