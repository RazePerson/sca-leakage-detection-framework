import numpy as np
from visualisation import DefaultPlotter, SeabornPlotter
from leak_calc import TVLA


class LeakageDetectionFramework:
    def __init__(self):
        self.default_plotter = DefaultPlotter()

    def load_data(self, data_file):
        self.data = np.load(data_file)

    def extract_dataset_components(self):
        self.traces = (self.data["traces"]).astype(float)
        self.flag = self.data["flag"]
        self.nr_of_traces, self.nr_of_samples = self.traces.shape

    def get_fixed_traces(self):
        tF_index = self.flag == 1
        return self.traces[tF_index[:, 0], :]

    def get_random_traces(self):
        tR_index = self.flag == 1
        return self.traces[tR_index[:, 0], :]

    def calculate_leakage(self, range, threshold, test_type=None):
        if test_type is not None:
            return 0
        else:
            tvla = TVLA()
            tvla.welch_t_statistic()
            self.threshold = threshold
            try:
                return np.abs(self.t_statistic[range]) > self.threshold
            except AttributeError:
                print("t_statistic is not set!")

    def create_default_plots(self):
        self.default_plotter.create_power_trace_plot(self)
        self.default_plotter.create_t_statistic_plot(self)

    def plot(self):
        self.default_plotter.plot()

    def __str__(self):
        return "Number of traces: %.0f\nNumber of samples: %.0f " % (
            self.nr_of_traces,
            self.nr_of_samples,
        )
