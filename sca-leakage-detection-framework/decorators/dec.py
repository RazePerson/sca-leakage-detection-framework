from data import TraceData
import pandas as pd


def translate_plot_data(func):
    def wrapper(self, data, x=None, y=None):
        if not isinstance(data, pd.DataFrame):
            x = x if x else "Length"
            y = y if y else "Data"
            data = TraceData.get_instance().convert_to_data_frame(data, x=x, y=y)
        func(self, data)
        return self

    return wrapper


def translate_plot_data_dist(func):
    def wrapper(self, data, label=None):
        if not isinstance(data, pd.Series):
            data = TraceData.get_instance().convert_to_series(data, label=label)
        func(self, data)
        return self

    return wrapper
