import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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
    def __init__(self, style=None):
        self.active_plots = []
        self.is_subplot = False
        self.ax_count = 0
        self.figsize = (7, 6)
        self.color = None
        style = style if style else "darkgrid"
        sns.set_theme(style=style)

    def change_color(self, color):
        self.color = color

    def default_color(self):
        self.color = None

    def hist_plot_traces(self, data):
        sns.histplot(data=data)

    def create_plot(self, data):
        sns.displot(data=data)

    # def create_line_plot(self, data):
    #     g = sns.FacetGrid(data, size=5, aspect=2.5)
    #     g.map(sns.relplot)

    #     self.active_plots.append(g)

    def create_line_plot(self, data, figsize=None):
        figsize = figsize if figsize else self.figsize
        x, y = data.columns.values
        if self.is_subplot is True:
            # self.active_plots.append(sns.relplot(x=x, y=y, data=data, kind="line"))
            # fig = plt.gcf()
            # fig.set_size_inches(7, 6)
            self.__handle_plot(
                sns.relplot(x=x, y=y, data=data, kind="line", color=self.color), figsize
            )
            self.ax_count += 1
        else:
            self.__handle_plot(
                sns.relplot(x=x, y=y, data=data, kind="line", color=self.color), figsize
            )
            # self.active_plots.append(sns.relplot(x=x, y=y, data=data, kind="line"))
            # fig = plt.gcf()
            # fig.set_size_inches(7, 6)

    def __handle_plot(self, plot_func, figsize):
        self.active_plots.append(plot_func)
        fig = plt.gcf()
        fig.set_size_inches(figsize)

    def create_hist_plot(self, data):
        # x, y = data.columns.values
        bins = np.arange(data.min(), data.max() + 1)
        if self.is_subplot is True:
            self.active_plots.append(sns.displot(data, bins=bins, kde=False))
            self.ax_count += 1
        else:
            self.active_plots.append(sns.displot(data, bins=bins, kde=False))

    # def draw_horizontal_line(self, y_coord, color=None, ls=None):
    #     color = color if color else "red"
    #     ls = ls if ls else "--"
    #     last_plot = len(self.active_plots) - 1
    #     print(self.active_plots[last_plot])
    #     print(self.active_plots[last_plot].axes[0])

    #     self.active_plots[last_plot].axes[0][0].axhline(y_coord, color=color, ls=ls)

    def draw_horizontal_line(self, y_coord, color=None, ls=None):
        color = color if color else "black"
        ls = ls if ls else "--"

        last_plot = len(self.active_plots) - 1

        axis = self.active_plots[last_plot].axes[0][0]
        axis.axhline(y_coord, color=color, ls=ls)

    def draw_vertical_line(self, x_coord, color=None, ls=None):
        color = color if color else "black"
        ls = ls if ls else "--"

        last_plot = len(self.active_plots) - 1

        axis = self.active_plots[last_plot].axes[0][0]
        axis.axvline(x_coord, color=color, ls=ls)

    def highlight_points(self, points, marker=None, color=None):
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

        # figsize = (30, 14)
        # plt.figure(figsize=figsize)
        plt.show()
