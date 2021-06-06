from decorators import translate_plot_data, translate_plot_data_dist
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Plotter:
    def change_color(self, color):
        self.change_color(color)

    def default_color(self):
        self.default_color()

    def show_threshold(self, threshold, color=None, ls=None):
        self.draw_horizontal_line(threshold, color=color, ls=ls)
        self.draw_horizontal_line(-threshold, color=color, ls=ls)
        return self

    def highlight_points(self, points, marker=None, color=None):
        pass

    def plot(self):
        pass

    def _extract_param(self, param_name, default_value, **params):
        if param_name in params:
            return params.get(param_name)
        else:
            return default_value


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
        plt.title("Figure %.0f: Fixed vs Random Exp.1 (%.0f traces)" % (self.fignum, ldf.nr_of_traces))
        self.fignum += 1

    def create_power_trace_plot(self, ldf):
        math_util = MathUtil()
        plt.figure(self.fignum)
        plt.clf()
        MT = math_util.mean(ldf.traces)
        plt.plot(MT)
        plt.xlim(0, ldf.nr_of_samples - 1)
        plt.xlabel("Time Samples")
        plt.ylabel("Norm. Power")
        plt.title("Figure %.0f: Power trace (as reference)" % self.fignum)
        self.fignum += 1

    def plot(self):
        plt.show()


class SeabornPlotter(Plotter):
    FIG_SIZE = "fig_size"

    def __init__(self, style=None):
        self.active_plots = []
        self.ax_count = 0
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

    @translate_plot_data
    def create_line_plot(self, data, **params):
        figsize = self._extract_param(self.FIG_SIZE, (7, 6), **params)
        x, y = data.columns.values
        self.__handle_plot(sns.relplot(x=x, y=y, data=data, kind="line", color=self.color), figsize)

    def __handle_plot(self, plot_func, figsize):
        self.active_plots.append(plot_func)
        fig = plt.gcf()
        fig.set_size_inches(figsize)

    @translate_plot_data_dist
    def create_hist_plot(self, data, **params):
        bins = np.arange(data.min(), data.max() + 1)
        self.active_plots.append(sns.displot(data, bins=bins, kde=False))
        return self

    def draw_horizontal_line(self, y_coord, color=None, ls=None):
        color = color if color else "black"
        ls = ls if ls else "--"

        last_plot = len(self.active_plots) - 1

        axis = self.active_plots[last_plot].axes[0][0]
        axis.axhline(y_coord, color=color, ls=ls)
        return self

    def draw_vertical_line(self, x_coord, color=None, ls=None):
        color = color if color else "black"
        ls = ls if ls else "--"

        last_plot = len(self.active_plots) - 1

        axis = self.active_plots[last_plot].axes[0][0]
        axis.axvline(x_coord, color=color, ls=ls)
        return self

    def highlight_points(self, points, marker=None, color=None):
        marker = marker if marker else "*"
        color = color if color else "red"
        for x, y in points:
            plt.plot(x, y, marker=marker, color=color)
        return self

    def plot(self):
        plt.show()
