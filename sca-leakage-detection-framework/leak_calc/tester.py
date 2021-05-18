from data import TVLAData, CorrelationTestData, SNRTestData
from leak_calc import MathUtil, TVLAResult, CorrelationTestResult, SNRTestResult
from tqdm import tqdm
import numpy as np


class Tester:
    def __init__(self):
        self.data_loader = None

    def execute_test(self, **params):
        pass

    def _extract_param(self, param_name, default_value, **params):
        if param_name in params:
            return params.get(param_name)
        else:
            return default_value


class TVLA(Tester):
    T_STAT_RANGE = "t_stat_range"
    THRESHOLD = "threshold"

    def __init__(self):
        self.data_loader = TVLAData.get_instance()

    def execute_test(self, **params):
        t_statistic = self.__welch_t_statistic(self.data_loader.get_every_fixed_trace(), self.data_loader.get_every_random_trace())

        t_stat_range = self._extract_param(self.T_STAT_RANGE, range(0, len(t_statistic)), **params)
        t_statistic = t_statistic[t_stat_range]
        threshold = self._extract_param(self.THRESHOLD, 4.5, **params)

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
    FOLDS_PARAM = "folds"
    BYTE_TO_FOCUS_PARAM = "byte_to_focus"

    def __init__(self):
        self.data_loader = CorrelationTestData.get_instance()
        self.math_util = MathUtil()

    def execute_test(self, **params):
        self.folds = self._extract_param(self.FOLDS_PARAM, 10, **params)
        self.byte_to_focus = self._extract_param(self.BYTE_TO_FOCUS_PARAM, 0, **params)

        self.__allocate_memory()
        self.__initialise_sets()
        self.__profile()
        corr_result = self.correlation_test()
        leaky_samples = np.array(range(len(corr_result)))
        leaky_samples = leaky_samples[corr_result]
        nr_of_leaky_points = len(leaky_samples)
        return CorrelationTestResult(leaky_samples=leaky_samples, nr_of_leaky_points=nr_of_leaky_points)

    def __allocate_memory(self):
        self.test_set = [None] * (2 * self.folds)
        self.profile_set = [None] * (2 * self.folds)

    def __initialise_sets(self):
        self.__init_to_zero()
        self.__init_sets_with_trace_values()
        # print("Test set: ", self.test_set)
        # print("Profile set: ", self.profile_set)

    def __init_to_zero(self):
        self.step = int(np.floor(self.data_loader.nr_of_traces / self.folds))
        for i in range(0, 2 * self.folds, 1):
            if np.mod(i, 2) == 0:
                # self.profile_set[i] and self.test_set[i] with even index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, self.data_loader.nr_of_samples))
                self.test_set[i] = np.zeros((self.step, self.data_loader.nr_of_samples))
            else:
                # self.profile_set[i] and self.test_set[i] with odd index i will contain traces:
                self.profile_set[i] = np.zeros(((self.folds - 1) * self.step, 16), dtype=np.int)
                self.test_set[i] = np.zeros((self.step, 16), dtype=np.int)

    def __init_sets_with_trace_values(self):
        t = 0
        for i in range(0, self.folds, 1):
            profile_set_ind = 0
            for j in range(0, self.folds, 1):
                trace_index = slice(j * self.step, (j + 1) * self.step)
                if i != j:
                    # Profile sets:
                    step_index = slice(profile_set_ind * self.step, (profile_set_ind + 1) * self.step)

                    self.profile_set[t][step_index, :] = self.data_loader.traces[trace_index, :]
                    self.profile_set[t + 1][step_index, :] = self.data_loader.plain_text[trace_index, :]
                    profile_set_ind = profile_set_ind + 1
                else:
                    # Test sets:
                    self.test_set[t] = self.data_loader.traces[trace_index, :]
                    self.test_set[t + 1] = self.data_loader.plain_text[trace_index, :]
            t = t + 2

    def __value_step(self, matrix, first, second):
        return matrix[first * self.step : second * self.step, :]

    def __profile(self):
        self.model = [None] * self.folds

        t = 0
        for j in range(0, self.folds, 1):
            Lj = self.profile_set[t]
            Pj = self.profile_set[t + 1]

            to_be_put_in_model = np.zeros((self.step, self.data_loader.nr_of_samples))

            for i in range(0, self.step, 1):
                to_be_put_in_model[i, :] = self.math_util.mean(Lj[Pj[:, self.byte_to_focus] == i, :])

            self.model[j] = to_be_put_in_model

            t = t + 2

    def correlation_test(self):
        rho = np.zeros((self.folds, self.data_loader.nr_of_samples))
        print("Rho shape: [%.0f][%.0f]" % (len(rho), len(rho[0])))

        number_of_traces_in_test_set = self.test_set[0].shape[0]

        for j in range(0, self.folds, 1):
            test_set = self.test_set[j * 2]
            model_set = self.model[j]
            rho[j, :] = self.__corrcoef(test_set, model_set)

        print("Traces in test set: ", number_of_traces_in_test_set)
        rho_total = self.math_util.mean(rho)
        rho_normalized = np.log((rho_total + 1) / (-rho_total + 1)) * np.sqrt(number_of_traces_in_test_set - 3) * 0.5

        print(rho_normalized)

        return np.abs(rho_normalized) > 4.5

    def __corrcoef(self, first_set, second_set):
        first_set_n = first_set - np.mean(first_set, axis=0)
        first_set_n = first_set_n / np.sqrt(np.sum(np.square(first_set_n), axis=0))
        second_set_n = second_set - second_set.mean(axis=0)
        second_set_n = second_set_n / np.sqrt(np.sum(np.square(second_set_n), axis=0))
        return np.sum(np.multiply(first_set_n, second_set_n), axis=0)

    def __set_shape(self, set_name, set):
        print("%s set: [%.0f][%.0f][%.0f] " % (set_name, len(set), len(set[0]), len(set[0][0])))


class SNRTest(Tester):
    LEAKAGE_MODEL = "leakage_model"
    TARGET_BYTE_PARAM = "target_byte"
    CORRECT_BYTE_VALUE_PARAM = "correct_byte_value"
    LSB = "LSB"
    LS2B = "LS2B"
    MSB = "MSB"
    HW = "HW"
    ID = "ID"

    def __init__(self):
        self.data_loader = SNRTestData.get_instance()
        self.math_util = MathUtil()

    def execute_test(self, **params):
        leakage_model = self._extract_param(self.LEAKAGE_MODEL, None, **params)
        if leakage_model is None:
            raise NameError('You must define the parameter "%s"!' % self.LEAKAGE_MODEL)

        self.target_byte = self._extract_param(self.TARGET_BYTE_PARAM, 0, **params)
        self.correct_byte_value = self._extract_param(self.CORRECT_BYTE_VALUE_PARAM, 0x00, **params)

        if leakage_model == self.LSB:
            result = self.__execute_lsb()
        elif leakage_model == self.LS2B:
            result = self.__execute_ls2b()
        elif leakage_model == self.MSB:
            result = self.__execute_msb()
        elif leakage_model == self.HW:
            result = self.__execute_hw()
        elif leakage_model == self.ID:
            result = self.__execute_id()

        return SNRTestResult(result)

    def __execute_lsb(self):
        label_LSB = []  # the label to divide the data
        for i in tqdm(range(0, self.data_loader.nr_of_traces)):
            label_LSB.append(self.SBOX[self.correct_byte_value ^ int(self.data_loader.plaintext[i][self.target_byte])] & 0b1)
        return self.__return_snr_trace(self.data_loader.traces, label_LSB)

    def __execute_ls2b(self):
        label_LS2B = []  # the label to divide the data
        for i in tqdm(range(0, self.data_loader.nr_of_traces)):
            label_LS2B.append(self.SBOX[self.correct_byte_value ^ int(self.data_loader.plaintext[i][self.target_byte])] & 0b11)
        return self.__return_snr_trace(self.data_loader.traces, label_LS2B)

    def __execute_msb(self):
        label_MSB = []  # the label to divide the data
        for i in tqdm(range(0, self.data_loader.nr_of_traces)):
            label_MSB.append(self.SBOX[self.correct_byte_value ^ int(self.data_loader.plaintext[i][self.target_byte])] & 0b10000000)

        return self.__return_snr_trace(self.data_loader.traces, label_MSB)

    def __execute_hw(self):
        label_HW = []  # the label to divide the data
        for i in tqdm(range(0, self.data_loader.nr_of_traces)):
            label_HW.append(self.__HW(self.SBOX[self.correct_byte_value ^ int(self.data_loader.plaintext[i][self.target_byte])]))
        return self.__return_snr_trace(self.data_loader.traces, label_HW)

    def __HW(self, x):
        return sum([x & (1 << i) > 0 for i in range(32)])

    def __execute_id(self):
        label_ID = []  # the label to divide the data
        for i in tqdm(range(0, self.data_loader.nr_of_traces)):
            label_ID.append(self.SBOX[self.correct_byte_value ^ int(self.data_loader.plaintext[i][self.target_byte])])
        return self.__return_snr_trace(self.data_loader.traces, label_ID)

    def __prepare_data(self, trace_set, labels_set):
        """
        trace_set = a set of traces
        labels_set = the leakage model of the target intermediate value

        returns a dictionary of the form
        'label_value': list of traces associated with 'label_value'
        """

        labels = np.unique(labels_set)
        # initialize the dictionary
        d = {}
        for i in labels:
            d[i] = []
        for count, label in enumerate(labels_set):
            d[label].append(trace_set[count])
        return d

    def __return_snr_trace(self, trace_set, labels_set):
        """
        trace_set = a set of traces
        labels_set = a set of labels of the same lenght as trace_set

        returns a dictionary of the form
        'label_value': mean_sample trace with 'label_value'
        """
        mean_trace = {}
        signal_trace = []
        noise_trace = []
        labels = np.unique(labels_set)  # determine the set of unique values for the leakage model
        # for LSB and MSB, labels ={0,1} and for HW, labels={0,1,2,3,4,5,6,7}
        grouped_traces = self.__prepare_data(trace_set, labels_set)  # we group the traces according to the label
        # compute the mean trace (the same are the signal traces)
        for i in labels:
            mean_trace[i] = self.math_util.mean(grouped_traces[i])
            signal_trace.append(mean_trace[i])
        # compute the noise trace
        for i in labels:
            for trace in grouped_traces[i]:
                noise_trace.append(trace - mean_trace[i])
        var_noise = self.math_util.variance(noise_trace)
        var_signal = self.math_util.variance(signal_trace)
        snr_trace = var_signal / var_noise
        return snr_trace

    SBOX = [
        0x63,
        0x7C,
        0x77,
        0x7B,
        0xF2,
        0x6B,
        0x6F,
        0xC5,
        0x30,
        0x01,
        0x67,
        0x2B,
        0xFE,
        0xD7,
        0xAB,
        0x76,
        0xCA,
        0x82,
        0xC9,
        0x7D,
        0xFA,
        0x59,
        0x47,
        0xF0,
        0xAD,
        0xD4,
        0xA2,
        0xAF,
        0x9C,
        0xA4,
        0x72,
        0xC0,
        0xB7,
        0xFD,
        0x93,
        0x26,
        0x36,
        0x3F,
        0xF7,
        0xCC,
        0x34,
        0xA5,
        0xE5,
        0xF1,
        0x71,
        0xD8,
        0x31,
        0x15,
        0x04,
        0xC7,
        0x23,
        0xC3,
        0x18,
        0x96,
        0x05,
        0x9A,
        0x07,
        0x12,
        0x80,
        0xE2,
        0xEB,
        0x27,
        0xB2,
        0x75,
        0x09,
        0x83,
        0x2C,
        0x1A,
        0x1B,
        0x6E,
        0x5A,
        0xA0,
        0x52,
        0x3B,
        0xD6,
        0xB3,
        0x29,
        0xE3,
        0x2F,
        0x84,
        0x53,
        0xD1,
        0x00,
        0xED,
        0x20,
        0xFC,
        0xB1,
        0x5B,
        0x6A,
        0xCB,
        0xBE,
        0x39,
        0x4A,
        0x4C,
        0x58,
        0xCF,
        0xD0,
        0xEF,
        0xAA,
        0xFB,
        0x43,
        0x4D,
        0x33,
        0x85,
        0x45,
        0xF9,
        0x02,
        0x7F,
        0x50,
        0x3C,
        0x9F,
        0xA8,
        0x51,
        0xA3,
        0x40,
        0x8F,
        0x92,
        0x9D,
        0x38,
        0xF5,
        0xBC,
        0xB6,
        0xDA,
        0x21,
        0x10,
        0xFF,
        0xF3,
        0xD2,
        0xCD,
        0x0C,
        0x13,
        0xEC,
        0x5F,
        0x97,
        0x44,
        0x17,
        0xC4,
        0xA7,
        0x7E,
        0x3D,
        0x64,
        0x5D,
        0x19,
        0x73,
        0x60,
        0x81,
        0x4F,
        0xDC,
        0x22,
        0x2A,
        0x90,
        0x88,
        0x46,
        0xEE,
        0xB8,
        0x14,
        0xDE,
        0x5E,
        0x0B,
        0xDB,
        0xE0,
        0x32,
        0x3A,
        0x0A,
        0x49,
        0x06,
        0x24,
        0x5C,
        0xC2,
        0xD3,
        0xAC,
        0x62,
        0x91,
        0x95,
        0xE4,
        0x79,
        0xE7,
        0xC8,
        0x37,
        0x6D,
        0x8D,
        0xD5,
        0x4E,
        0xA9,
        0x6C,
        0x56,
        0xF4,
        0xEA,
        0x65,
        0x7A,
        0xAE,
        0x08,
        0xBA,
        0x78,
        0x25,
        0x2E,
        0x1C,
        0xA6,
        0xB4,
        0xC6,
        0xE8,
        0xDD,
        0x74,
        0x1F,
        0x4B,
        0xBD,
        0x8B,
        0x8A,
        0x70,
        0x3E,
        0xB5,
        0x66,
        0x48,
        0x03,
        0xF6,
        0x0E,
        0x61,
        0x35,
        0x57,
        0xB9,
        0x86,
        0xC1,
        0x1D,
        0x9E,
        0xE1,
        0xF8,
        0x98,
        0x11,
        0x69,
        0xD9,
        0x8E,
        0x94,
        0x9B,
        0x1E,
        0x87,
        0xE9,
        0xCE,
        0x55,
        0x28,
        0xDF,
        0x8C,
        0xA1,
        0x89,
        0x0D,
        0xBF,
        0xE6,
        0x42,
        0x68,
        0x41,
        0x99,
        0x2D,
        0x0F,
        0xB0,
        0x54,
        0xBB,
        0x16,
    ]
