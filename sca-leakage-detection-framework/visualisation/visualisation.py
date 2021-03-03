import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from leak_calc import MathUtil


class DefaultPlotter:

    fignum = 1

    def create_t_statistic_plot(self, ldf):
        plt.figure(self.fignum)
        plt.clf()
        plt.plot(ldf.t_statistic)
        plt.plot([0, ldf.nr_of_samples - 1], [ldf.threshold, ldf.threshold], "--r")
        plt.plot([0, ldf.nr_of_samples - 1], [-ldf.threshold, -ldf.threshold], "--r")
        plt.xlim(0, ldf.nr_of_samples - 1)
        plt.xlabel("Time Samples")
        plt.ylabel("t-statistic")
        plt.title(
            "Figure %.0f: Fixed vs Random Exp.1 (%.0f traces)"
            % (self.fignum, ldf.nr_of_traces)
        )
        self.fignum += 1

    def create_power_trace_plot(self, ldf):
        math_util = MathUtil()
        plt.figure(self.fignum)
        plt.clf()
        # MT = np.mean(ldf.traces,axis=0)
        MT = math_util.mean(ldf.traces)
        plt.plot(MT)
        plt.xlim(0, ldf.nr_of_samples - 1)
        plt.xlabel("Time Samples")
        plt.ylabel("Norm. Power")
        plt.title("Figure %.0f: Power trace (as reference)" % self.fignum)
        self.fignum += 1

    def plot(self):
        plt.show()


class SeabornPlotter:
    def __init__(self):
        sns.set_theme(style="darkgrid")

    def hist_plot_traces(self, data):
        sns.histplot()

    def create_plot(self, data):
        sns.displot(data)

    def create_plot_line(self, data):
        sns.relplot(data=data)

    def plot(self):
        plt.show()