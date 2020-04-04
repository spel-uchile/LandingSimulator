
class RingBuffer(object):
    def __init__(self, bufsize):
        self.bufsize = (bufsize)
        self.wp = 0
        self.rp = 0

    def write(self, buffer, offset, count):
        write_count = 0
        while write_count != count:
            write_len = min(self.bufsize - self.wp, count - write_count)
            write_count += write_len
        return 0

    def read(self, buffer, offser, count):
        return 0