from data import TVLAData
import pandas as pd


def __extract_param(param_name, default_value, **params):
    if param_name in params:
        return params.get(param_name)
    else:
        return default_value


def translate_plot_data(func):
    def wrapper(self, data, **params):
        if not isinstance(data, pd.DataFrame):
            x = __extract_param("x", "Length", **params)
            y = __extract_param("y", "Data", **params)
            data = TVLAData.get_instance().convert_to_data_frame(data, x=x, y=y)
        func(self, data, **params)
        return self

    return wrapper


def translate_plot_data_dist(func):
    def wrapper(self, data, **params):
        if not isinstance(data, pd.Series):
            label = __extract_param("label", None, **params)
            data = TVLAData.get_instance().convert_to_series(data, label=label)
        func(self, data, **params)
        return self

    return wrapper
