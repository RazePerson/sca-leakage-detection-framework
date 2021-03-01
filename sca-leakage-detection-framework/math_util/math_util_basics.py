import numpy as np

class MathUtil():

    def mean(self, data, indices=None, axis=None):
        final_data, final_axis = self.get_final_parameters(data, indices, axis)

        return np.mean(final_data, axis=final_axis)

    def variance(self, data, indices=None, axis=None):

        final_data, final_axis = self.get_final_parameters(data, indices, axis)

        return np.var(final_data, final_axis)


    def get_final_parameters(self, data, indices, axis):
        if indices is not None:
            final_data = data[indices[:,0],:]
        else:
            final_data = data
        
        if axis is not None:
            final_axis = axis
        else:
            final_axis = 0

        return final_data, final_axis