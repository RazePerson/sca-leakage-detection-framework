from data import TVLAData, CorrelationTestData
from leak_calc import MathUtil, TVLAResult
import numpy as np


class Tester:
    def __init__(self):
        self.data_loader = None

    def execute_test():
        pass


class TVLA(Tester):
    def __init__(self):
        self.data_loader = TVLAData.get_instance()

    def execute_test(self, t_stat_range=None, threshold=None):
        t_statistic = self.__welch_t_statistic(self.data_loader.get_fixed_traces(), self.data_loader.get_random_traces())
        t_stat_range = t_stat_range if t_stat_range else range(0, len(t_statistic))
        t_statistic = t_statistic[t_stat_range]
        threshold = threshold if threshold else 4.5
        leaky_indices = self.__leaky_indices(t_statistic, threshold)

        return TVLAResult(
            t_statistic=t_statistic,
            leaky_indices=leaky_indices,
            nr_of_leaky_points=len(leaky_indices),
            leaky_samples=t_statistic[leaky_indices],
        )

    def __welch_t_statistic(self, trace_set1, trace_set2):

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

    def __leaky_indices(self, t_statistic, threshold):
        leakage = np.abs(t_statistic) > threshold
        indices = np.array(range(len(leakage)))
        return indices[leakage]


class CorrelationTest(Tester):
    def __init__(self):
        self.data_loader = CorrelationTestData.get_instance()
