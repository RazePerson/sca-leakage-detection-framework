import numpy as np
from data import TVLAData


class PTest:
    def __init__(self, folds, poi):
        self.folds = folds
        self.poi = poi
        self.allocate_memory()
        self.initialise_sets()

    def allocate_memory(self):
        self.test_set = [None] * (2 * self.folds)
        self.profile_set = [None] * (2 * self.folds)

    def initialise_sets(self, t_test_data):
        self.init_to_zero(t_test_data)

    def init_to_zero(self):
        t_test_data = TVLAData.get_instance()
        self.step = int(np.floor(t_test_data.nr_of_traces / self.folds))
        for i in range(0, 2 * self.folds, 1):
            if np.mod(i, 2) == 0:
                # self.profile_set[i] and self.test_set[i] with even index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, t_test_data.nr_of_samples))
                self.test_set[i] = np.zeros((self.step, t_test_data.nr_of_samples))
            else:
                # self.profile_set[i] and self.test_set[i] with odd index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, 16), dtype=np.int)
                self.test_set[i] = np.zeros((self.step, 16), dtype=np.int)

    def init_sets_with_values(self, t_test_data):
        t = 0
        for i in range(0, self.folds, 1):
            q_in_profile_set = 0
            for j in range(0, self.folds, 1):
                if i != j:
                    # Profile sets:
                    self.profile_set[t][
                        q_in_profile_set * self.step : (q_in_profile_set + 1) * self.step,
                        :,
                    ] = t_test_data.traces[j * self.step : (j + 1) * self.step, :]
                    self.profile_set[t + 1][
                        q_in_profile_set * self.step : (q_in_profile_set + 1) * self.step,
                        :,
                    ] = t_test_data.plain_text[j * self.step : (j + 1) * self.step, :]
                    q_in_profile_set = q_in_profile_set + 1
                else:
                    # Test sets:
                    self.test_set[t] = t_test_data.traces[j * self.step : (j + 1) * self.step, :]
                    self.test_set[t + 1] = t_test_data.plain_text[j * self.step : (j + 1) * self.step, :]
            t = t + 2

    def value_step(self, matrix, first, second):
        return matrix[first * self.step : second * self.step, :]

    def profile(self):
        # Number of traces in a profile set:
        nr_traces_profile_set = len(self.profile_set[0][:, 0])

        # Initialise the matrix with profiles:
        mu = [None] * self.step

        t = 0
        for j in range(0, self.step, 1):
            # Temporary Profile set (traces and plaintext)
            Lj = self.profile_set[t]
            Pj = self.profile_set[t + 1]

            to_be_put_in_mu = np.zeros((256, Nsamples))

            # Compute the mean of j-th profile set:
            for i in range(0, 256, 1):
                to_be_put_in_mu[i, :] = np.mean(Lj[Pj[:, Byte_to_focus] == i, :], axis=0)

            mu[j] = to_be_put_in_mu

            t = t + 2