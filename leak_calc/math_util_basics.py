import numpy as np


class MathUtil:
    def mean(self, data, axis=None):
        axis = axis if axis else 0
        return np.mean(data, axis=axis)

    def variance(self, data, axis=None):
        axis = axis if axis else 0
        return np.var(data, axis=axis)
