

class PowerPort(object):
    def __init__(self, port_id, current_limit, component_base):
        self.port_id = port_id
        self.current_limit = current_limit
        self.component_base = component_base
        self.set_voltage(-1)

    def get_current(self):
        current = self.component_base

    def set_voltage(self, voltage):
        if voltage_ == voltage:
            return
        voltage_ = voltage