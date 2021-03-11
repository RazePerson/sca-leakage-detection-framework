import numpy as np
import pandas as pd
from IPython.display import display 
from visualisation import SeabornPlotter
from leak_calc import TVLA
from data import TraceData


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

    def calculate_leakage(self, t_statistic, range, threshold):
        try:
            return np.abs(t_statistic[range]) > threshold
        except AttributeError:
            print("t_statistic is not set!")

    def convert_t_statistic_to_data_frame(self, data):
        return pd.DataFrame({'T-Statistic': data, 'Time Samples': range(0, len(data))})

    def plotter(self):
        return self.Plotter()

    def __str__(self):
        return "Number of traces: %.0f\nNumber of samples: %.0f " % (
            self.nr_of_traces,
            self.nr_of_samples,
        )

    class Plotter():
        def __init__(self):
            self.visualisation = SeabornPlotter()

        def create_plot(self, data):
            self.visualisation.create_plot_line(data)
            return self

        def show_threshold(self, threshold, color=None):
            self.visualisation.draw_horizontal_line(threshold)
            self.visualisation.draw_horizontal_line(-threshold)
            return self

        def mark_points(self, points):
            self.visualisation.mark_points(points)
            return self

        def subplot(self, row, col):
            self.visualisation.subplot(row, col)
            return self

        def plot(self):
            self.visualisation.plot()
