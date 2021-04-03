from visualisation import SeabornPlotter
from decorators import translate_plot_data


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

    @translate_plot_data
    def create_hist_plot(self, data, x=None, y=None):
        self.visualisation.create_hist_plot(data)
        return self

    def show_threshold(self, threshold, color=None):
        self.visualisation.draw_horizontal_line(threshold)
        self.visualisation.draw_horizontal_line(-threshold)
        return self

    def highlight_points(self, points, marker=None, color=None):
        self.visualisation.highlight_points(points, marker=marker, color=color)
        return self

    def subplot(self, row, col):
        self.visualisation.subplot(row, col)
        return self

    def plot(self):
        self.visualisation.plot()
