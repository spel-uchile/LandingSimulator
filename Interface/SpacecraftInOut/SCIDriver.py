
from .Ports.SCIPort import SCIPort


class SCIDriver(object):
    def __init__(self):
        self.ports = {}

    def connect_port(self, port_id, tx_buf_size, rx_buf_size):
        # port already used
        if str(port_id) in self.ports.keys():
            return -1
        self.ports[str(port_id)] = SCIPort(tx_buf_size, rx_buf_size)
        return 0

    def close_port(self, port_id):
        # Port no used
        if str(port_id) not in self.ports.keys():
            return -1
        del self.ports[str(port_id)]

    def send_to_sim(self, port_id, buffer, offset, count):
        if str(port_id) not in self.ports.keys():
            return -1
        port = self.ports[str(port_id)]
        return port.write_tx(buffer, offset, count)

    def send_to_spacecraft(self, port_id, buffer, offset, count):
        if str(port_id) not in self.ports.keys():
            return -1
        port = self.ports[str(port_id)]
        return port.write_rx(buffer, offset, count)

    def received_from_sim(self, port_id, buffer, offset, count):
        if str(port_id) not in self.ports.keys():
            return -1
        port = self.ports[str(port_id)]
        return port.read_rx(buffer, offset, count)

    def received_from_spacecraft(self, port_id, buffer, offset, count):
        if str(port_id) not in self.ports.keys():
            return -1
        port = self.ports[str(port_id)]
        return port.read_tx(buffer, offset, count)





