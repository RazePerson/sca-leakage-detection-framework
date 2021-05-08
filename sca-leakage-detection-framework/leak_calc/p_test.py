import numpy as np
from data import TVLAData


class PTest:
    def __init__(self, folds, poi, byte_to_focus):
        self.folds = folds
        self.poi = poi
        self.byte_to_focus = byte_to_focus
        self.allocate_memory()
        self.initialise_sets()

    def allocate_memory(self):
        self.test_set = [None] * (2 * self.folds)
        self.profile_set = [None] * (2 * self.folds)

    def initialise_sets(self, trace_data):
        self.init_to_zero(trace_data)
        self.init_sets_with_trace_values(trace_data)

    def init_to_zero(self):
        trace_data = TVLAData.get_instance()
        self.step = int(np.floor(trace_data.nr_of_traces / self.folds))
        for i in range(0, 2 * self.folds, 1):
            if np.mod(i, 2) == 0:
                # self.profile_set[i] and self.test_set[i] with even index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, trace_data.nr_of_samples))
                self.test_set[i] = np.zeros((self.step, trace_data.nr_of_samples))
            else:
                # self.profile_set[i] and self.test_set[i] with odd index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, 16), dtype=np.int)
                self.test_set[i] = np.zeros((self.step, 16), dtype=np.int)

    def init_sets_with_trace_values(self, trace_data):
        t = 0
        for i in range(0, self.folds, 1):
            profile_set_ind = 0
            for j in range(0, self.folds, 1):
                trace_slice = slice(j * self.step, (j + 1) * self.step)
                if i != j:
                    # Profile sets:
                    step_slice = slice(profile_set_ind * self.step, (profile_set_ind + 1) * self.step)
                    self.profile_set[t][step_slice, :] = trace_data.traces[trace_slice, :]
                    self.profile_set[t + 1][step_slice, :] = trace_data.plain_text[trace_slice, :]
                    profile_set_ind = profile_set_ind + 1
                else:
                    # Test sets:
                    self.test_set[t] = trace_data.traces[trace_slice, :]
                    self.test_set[t + 1] = trace_data.plain_text[trace_slice, :]
            t = t + 2

    def value_step(self, matrix, first, second):
        return matrix[first * self.step : second * self.step, :]

    def profile(self, trace_data):
        # Initialise the matrix with profiles:
        self.model = [None] * self.step

        t = 0
        for j in range(0, self.step, 1):
            # Temporary Profile set (traces and plaintext)
            Lj = self.profile_set[t]
            Pj = self.profile_set[t + 1]

            to_be_put_in_model = np.zeros((256, trace_data.nr_of_samples))

            # Compute the mean of j-th profile set:
            for i in range(0, 256, 1):
                to_be_put_in_model[i, :] = np.mean(Lj[Pj[:, self.byte_to_focus] == i, :], axis=0)

            self.model[j] = to_be_put_in_model

            t = t + 2

    def correlation_test(self, trace_data):
        rhoj = np.zeros((self.step, trace_data.nr_of_samples))

        for j in range(0, self.step, 1):
            rhoj[j, :] = np.corrcoef(self.model[j], self.test_set[j * 2])

        number_of_traces_in_test_set = self.test_set[0].shape[0]
        rho_total = np.mean(rhoj, axis=0)
        rho_normalized = np.log((rho_total + 1) / (-rho_total + 1)) * np.sqrt(number_of_traces_in_test_set - 3) * 0.5

        return np.abs(rho_normalized) > 4.5
