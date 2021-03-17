import numpy as np
from leak_calc import TVLA
from data import TraceData
from core.plotter import Plotter


class LeakageDetectionFramework:
    # def __init__(self):
    #     self.default_plotter = DefaultPlotter()

    def load_data(self, data_file):
        data = np.load(data_file)
        trace_data = TraceData.get_instance()
        trace_data.initialise(data)

    def calculate_t_statistic(self, test_type=None):
        trace_data = TraceData.get_instance()
        if test_type is not None:
            return 0
        else:
            tvla = TVLA()
            return tvla.welch_t_statistic(
                trace_data.get_fixed_traces(), trace_data.get_random_traces()
            )

    def indices_of_leaky_samples(self, t_statistic, range, threshold):
        try:
            return np.abs(t_statistic[range]) > threshold
        except AttributeError:
            print("t_statistic is not set!")

    def plotter(self):
        return Plotter()
