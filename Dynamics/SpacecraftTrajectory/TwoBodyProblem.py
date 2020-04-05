# Elias Obreque

import numpy as np


class TwoBodyProblem(object):
    def __init__(self, mu, timestep, init_position, init_velocity):
        self.position_i = init_position
        self.velocity_i = init_velocity
        self.acc_i      = np.zeros(3)
        self.mu         = mu
        self.step_width = timestep
        self.current_time = 0

    def update_state(self, time_array):
        self.rungeonestep()
        return self.position_i, self.velocity_i

    def dynamics(self, state, t):
        x = state[0]
        y = state[1]
        z = state[2]

        vx = state[3]
        vy = state[4]
        vz = state[5]

        r3 = np.linalg.norm(state[0:3]) ** 3

        rhs = np.zeros(6)
        rhs[0] = vx
        rhs[1] = vy
        rhs[2] = vz
        rhs[3] = -self.mu * x / r3 + self.acc_i[0]
        rhs[4] = -self.mu * y / r3 + self.acc_i[1]
        rhs[5] = -self.mu * z / r3 + self.acc_i[2]
        return rhs

    def set_acc_i(self, acc_i):
        self.acc_i += acc_i

    def rungeonestep(self):
        t = self.current_time
        dt = self.step_width

        x = np.concatenate((self.position_i, self.velocity_i))

        k1 = self.dynamics(x, t)
        xk2 = x + (dt / 2.0) * k1

        k2 = self.dynamics(xk2, (t + dt / 2.0))
        xk3 = x + (dt / 2.0) * k2

        k3 = self.dynamics(xk3, (t + dt / 2.0))
        xk4 = x + dt * k3

        k4 = self.dynamics(xk4, (t + dt))

        next_x = x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        self.current_time += self.step_width
        self.position_i = np.array(next_x[0:3])
        self.velocity_i = np.array(next_x[3:6])
