import numpy as np
from visualisation import (DefaultPlotter, SeabornPlotter)
from math_util import MathUtil

class LeakageDetectionFramework():

    def __init__(self):
        self.default_plotter = DefaultPlotter()
    
    def load_data(self, data_file):
        self.data = np.load(data_file)

    def extract_dataset_components(self):
        self.traces = (self.data['traces']).astype(float)
        self.flag = self.data['flag']
        self.nr_of_traces, self.nr_of_samples = self.traces.shape

    def welch_t_statistic(self):
        tF_index = self.flag==1;
        tR_index = self.flag==0;

        NF = tF_index.sum()
        NR = tR_index.sum()

        math_util = MathUtil()

        meanF = math_util.mean(self.traces, tF_index);
        meanR = math_util.mean(self.traces, tR_index);
        varF = math_util.variance(self.traces, tF_index);
        varR = math_util.variance(self.traces, tR_index);

        self.t_statistic  = (meanF - meanR)/np.sqrt(varF/NF + varR/NR)

    def calculate_leakage(self, range, threshold):
        self.threshold = threshold
        try:
            return np.abs(self.t_statistic[range]) > self.threshold
        except AttributeError:
            print('t_statistic is not set!')

    def create_default_plots(self):
        self.default_plotter.create_power_trace_plot(self)
        self.default_plotter.create_t_statistic_plot(self)
    
    def plot(self):
        self.default_plotter.plot()

    def __str__(self):
        return 'Number of traces: %.0f\nNumber of samples: %.0f ' % (self.nr_of_traces, self.nr_of_samples)