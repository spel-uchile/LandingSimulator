"""
Created: 5/11/2020
Autor: Elias Obreque Sepulveda
email: els.obrq@gmail.com

"""
import numpy as np


class ThrusterODE(object):
    def __init__(self, step_width, ign_time, lag_coef, max_t):
        self.step_width = step_width
        self.lag_coef = lag_coef
        self.ign_time = ign_time
        self.current_time = 0
        self.thr_is_on = 0
        self.target_mag_thrust_c = 0
        self.current_mag_thrust_c = 0

    def get_mag_thrust_c(self):
        return self.current_mag_thrust_c

    def dynamics_thrust(self, state, t):
        rhs_ = (self.target_mag_thrust_c - state) / self.lag_coef
        return rhs_

    def update_ode(self):
        self.rungeonestep()

    def rungeonestep(self):
        x = self.current_mag_thrust_c
        t = self.current_time
        dt = self.step_width

        k1 = self.dynamics_thrust(x, t)
        xk2 = x + (dt / 2.0) * k1

        k2 = self.dynamics_thrust(xk2, (t + dt / 2.0))
        xk3 = x + (dt / 2.0) * k2

        k3 = self.dynamics_thrust(xk3, (t + dt / 2.0))
        xk4 = x + dt * k3

        k4 = self.dynamics_thrust(xk4, (t + dt))

        next_x = x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        self.current_time += self.step_width
        self.current_mag_thrust_c = next_x

    def set_burn_time(self, burn_time):
        self.max_burn_time = burn_time

    def set_target_mag_thrust(self, value):
        self.target_mag_thrust_c = value

    def set_lag_coef(self, lag_coef):
        self.lag_coef = lag_coef