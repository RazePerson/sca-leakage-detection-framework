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

    def calculate_t_statistic(self):
        trace_data = TraceData.get_instance()
        tvla = TVLA()
        return tvla.welch_t_statistic(
            trace_data.get_fixed_traces(), trace_data.get_random_traces()
        )

    def indices_of_leaky_samples(self, t_statistic, t_stat_range, threshold):
        try:
            return self.__calculate_leakage(t_statistic, t_stat_range, threshold)
        except AttributeError:
            print("t_statistic is not set!")

    def number_of_leaky_points(self, t_statistic, t_stat_range, threshold):
        try:
            leakage = self.__calculate_leakage(t_statistic, t_stat_range, threshold)
            leaky_indices = leakage == True
            return leakage[leaky_indices].sum()
        except AttributeError:
            print("t_statistic is not set!")

    def calculate_leaky_points(self, t_statistic, t_stat_range, threshold):
        try:
            leakage = self.__calculate_leakage(t_statistic, t_stat_range, threshold)
            leaky_indices = leakage == True
            reduced_t_stat = t_statistic[t_stat_range]
            return reduced_t_stat[leaky_indices]
        except AttributeError:
            print("t_statistic is not set!")

    def __calculate_leakage(self, t_statistic, t_stat_range, threshold):
        return np.abs(t_statistic[t_stat_range]) > threshold

    def plotter(self, style=None):
        return Plotter(style)
