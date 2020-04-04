
import numpy as np


class RandomWalk(object):
    def __init__(self, step_width, std_dev, limit):
        self.step_width = step_width
        self.std_dev = std_dev
        self.limit = limit
        self.rhs = np.zeros(3)

    def __call__(self, *args, **kwargs):
        return self.rhs