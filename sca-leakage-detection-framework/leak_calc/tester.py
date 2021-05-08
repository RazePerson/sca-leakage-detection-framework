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
        t_statistic = self.__welch_t_statistic(self.data_loader.get_every_fixed_trace(), self.data_loader.get_every_random_trace())
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

    def execute_test(self, folds=None, byte_to_focus=None):
        self.folds = folds if folds else 1
        self.byte_to_focus = byte_to_focus if byte_to_focus else 1
        self.allocate_memory()
        self.initialise_sets()
        print(self.test_set)
        # self.profile()
        # return self.correlation_test()

    def allocate_memory(self):
        self.test_set = [None] * (2 * self.folds)
        self.profile_set = [None] * (2 * self.folds)

    def initialise_sets(self):
        self.init_to_zero()
        self.init_sets_with_trace_values()

    def init_to_zero(self):
        self.step = int(np.floor(self.data_loader.nr_of_traces / self.folds))
        print(self.step)
        for i in range(0, 2 * self.folds, 1):
            if np.mod(i, 2) == 0:
                # self.profile_set[i] and self.test_set[i] with even index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, self.data_loader.nr_of_samples))
                self.test_set[i] = np.zeros((self.step, self.data_loader.nr_of_samples))
            else:
                # self.profile_set[i] and self.test_set[i] with odd index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, 16), dtype=np.int)
                self.test_set[i] = np.zeros((self.step, 16), dtype=np.int)

    def init_sets_with_trace_values(self):
        t = 0
        for i in range(0, self.folds, 1):
            profile_set_ind = 0
            for j in range(0, self.folds, 1):
                trace_slice = slice(j * self.step, (j + 1) * self.step)
                if i != j:
                    # Profile sets:
                    step_slice = slice(profile_set_ind * self.step, (profile_set_ind + 1) * self.step)
                    self.profile_set[t][step_slice, :] = self.data_loader.traces[trace_slice, :]
                    self.profile_set[t + 1][step_slice, :] = self.data_loader.plain_text[trace_slice, :]
                    profile_set_ind = profile_set_ind + 1
                else:
                    # Test sets:
                    self.test_set[t] = self.data_loader.traces[trace_slice, :]
                    self.test_set[t + 1] = self.data_loader.plain_text[trace_slice, :]
            t = t + 2

    def value_step(self, matrix, first, second):
        return matrix[first * self.step : second * self.step, :]

    def profile(self):
        # Initialise the matrix with profiles:
        self.model = [None] * self.step

        t = 0
        for j in range(0, self.step, 1):
            # Temporary Profile set (traces and plaintext)
            Lj = self.profile_set[t]
            Pj = self.profile_set[t + 1]

            to_be_put_in_model = np.zeros((256, self.data_loader.nr_of_samples))

            # Compute the mean of j-th profile set:
            for i in range(0, 256, 1):
                to_be_put_in_model[i, :] = np.mean(Lj[Pj[:, self.byte_to_focus] == i, :], axis=0)

            self.model[j] = to_be_put_in_model

            t = t + 2

    def correlation_test(self):
        rhoj = np.zeros((self.step, self.data_loader.nr_of_samples))

        for j in range(0, self.step, 1):
            rhoj[j, :] = np.corrcoef(self.model[j], self.test_set[j * 2])

        number_of_traces_in_test_set = self.test_set[0].shape[0]
        rho_total = np.mean(rhoj, axis=0)
        rho_normalized = np.log((rho_total + 1) / (-rho_total + 1)) * np.sqrt(number_of_traces_in_test_set - 3) * 0.5

        return np.abs(rho_normalized) > 4.5
