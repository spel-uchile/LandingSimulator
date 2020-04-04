
from Dynamics.ClockGenerator import ClockGenerator


class ComponentBase(object):
    def __init__(self, prescalar_time):
        self.prescalar = prescalar_time
        self.isOn = True

    def set_power_state(self, port_id, voltage):
        self.isOn = voltage > 0.0
        return

    def get_current(self):
        return 0.0

    def main_routine(self, count):
        return

    def tick(self, count):
        if self.isOn is False:
            return
        if count % self.prescalar > 0:
            return
        self.main_routine(count)
        return

    def log_value(self):
        return
