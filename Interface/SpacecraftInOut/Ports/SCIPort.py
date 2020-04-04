
from ..Utils.RingBuffer import RingBuffer


class SCIPort(object):
    def __init__(self, rx_buf_size, tx_buf_size):
        self.rxb = RingBuffer(rx_buf_size)
        self.txb = RingBuffer(tx_buf_size)

    def write_rx(self, buffer, offset, count):
        return self.rxb.write(buffer, offset, count)

    def write_tx(self, buffer, offset, count):
        return self.txb.write(buffer, offset, count)

    def read_rx(self, buffer, offset, count):
        return self.rxb.read(buffer, offset, count)

    def read_tx(self, buffer, offset, count):
        return self.txb.read(buffer, offset, count)
