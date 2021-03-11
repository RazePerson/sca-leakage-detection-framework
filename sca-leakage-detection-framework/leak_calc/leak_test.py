from leak_calc import MathUtil
import numpy as np


class TVLA:
    def __init__(self):
        self.stuff = 0

    def welch_t_statistic(self, trace_set1, trace_set2):

        trace_set1_length = len(trace_set1)
        trace_set2_length = len(trace_set2)

        math_util = MathUtil()

        trace_set1_mean = math_util.mean(trace_set1)
        trace_set2_mean = math_util.mean(trace_set2)
        trace_set_1_var = math_util.variance(trace_set1)
        trace_set_2_var = math_util.variance(trace_set2)

        mean_diff = trace_set1_mean - trace_set2_mean

        var_per_length_1 = trace_set_1_var / trace_set1_length
        var_per_length_2 = trace_set_2_var / trace_set2_length

        return (mean_diff) / np.sqrt(var_per_length_1 + var_per_length_2)

    def correlation_test(self):
        pass