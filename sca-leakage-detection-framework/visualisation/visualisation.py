import matplotlib.pyplot as plt
import seaborn as sns
from leak_calc import MathUtil

sns.set()


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
        self.active_plots = []
        self.is_subplot = False
        self.ax_count = 0
        sns.set_theme(style="darkgrid")

    def hist_plot_traces(self, data):
        sns.histplot(data=data)

    def create_plot(self, data):
        sns.displot(data=data)

    def create_plot_line(self, data):
        y, x = data.columns.values
        if self.is_subplot is True:
            self.active_plots.append(
                sns.regplot(ax=self.axes[self.ax_count], x=x, y=y, data=data)
            )
            self.ax_count += 1
        else:
            self.active_plots.append(sns.relplot(x=x, y=y, data=data, kind="line"))

    def draw_horizontal_line(self, y_coord, color=None, ls=None):
        color = color if color else "red"
        ls = ls if ls else "--"

        last_plot = len(self.active_plots) - 1
        print(self.active_plots[last_plot].axes[0])
        axis = self.active_plots[last_plot].axes[0][0]
        axis.axhline(y_coord, color=color, ls=ls)

    def mark_points(self, points, marker=None, color=None):
        marker = marker if marker else "*"
        color = color if color else "red"
        for x, y in points:
            plt.plot(x, y, marker=marker, color=color)

    def subplot(self, row, col):
        self.fig, self.axes = plt.subplots(
            row, col, figsize=(10 * row, 3 * col), sharex=True
        )
        self.is_subplot = True

    def plot(self):
        plt.show()
