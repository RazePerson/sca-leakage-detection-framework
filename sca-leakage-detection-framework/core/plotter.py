from visualisation import SeabornPlotter
from decorators import translate_plot_data, translate_plot_data_dist


class Plotter:
    def __init__(self, style=None):
        self.visualisation = SeabornPlotter(style)

    def change_color(self, color):
        self.visualisation.change_color(color)

    def default_color(self):
        self.visualisation.default_color()

    @translate_plot_data
    def create_line_plot(self, data, x=None, y=None):
        self.visualisation.create_line_plot(data)
        return self

    @translate_plot_data_dist
    def create_hist_plot(self, data, x=None, y=None):
        self.visualisation.create_hist_plot(data)
        return self

    def show_threshold(self, threshold, color=None, ls=None):
        self.visualisation.draw_horizontal_line(threshold, color=color, ls=ls)
        self.visualisation.draw_horizontal_line(-threshold, color=color, ls=ls)
        return self

    def draw_horizontal_line(self, line, color=None, ls=None):
        self.visualisation.draw_horizontal_line(line, color=color, ls=ls)
        return self

    def draw_vertical_line(self, line, color=None, ls=None):
        self.visualisation.draw_vertical_line(line, color=color, ls=ls)
        return self

    def highlight_points(self, points, marker=None, color=None):
        self.visualisation.highlight_points(points, marker=marker, color=color)
        return self

    def subplot(self, row, col):
        self.visualisation.subplot(row, col)
        return self

    def plot(self):
        self.visualisation.plot()
