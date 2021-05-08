import pandas as pd
import numpy as np


class TraceData:
    def load_data(self, data_file):
        pass


class TVLAData(TraceData):
    __instance = None

    @staticmethod
    def get_instance():
        if TVLAData.__instance is None:
            TVLAData()
        return TVLAData.__instance

    def __init__(self):
        if TVLAData.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            TVLAData.__instance = self

    def load_data(self, data_file):
        data = np.load(data_file)
        self.data = data
        self.extract_dataset_components()

    def extract_dataset_components(self):
        self.traces = (self.data["traces"]).astype(float)
        self.flag = self.data["flag"]
        self.plain_text = self.data["pt"]
        self.nr_of_traces, self.nr_of_samples = self.traces.shape

    def get_all_traces(self):
        return self.traces

    def get_trace_sample(self, sample):
        return self.traces[:, sample]

    def get_every_fixed_trace(self):
        fixed_trace_index = self.flag == 1
        return self.traces[fixed_trace_index[:, 0], :]

    def get_fixed_trace_sample(self, sample):
        return self.get_every_fixed_trace()[:, sample]

    def get_every_random_trace(self):
        random_trace_index = self.flag == 0
        return self.traces[random_trace_index[:, 0], :]

    def get_random_trace_sample(self, sample):
        return self.get_every_random_trace()[:, sample]

    def convert_t_statistic_to_data_frame(self, data):
        return self.convert_to_data_frame(data_y=data, x="Time Samples", y="T-Statistic")

    def convert_to_data_frame(self, data_y, data_x=None, x=None, y=None):
        x = x if x else "Length"
        y = y if y else "Data"
        if not data_x:
            return pd.DataFrame({x: range(0, len(data_y)), y: data_y})
        else:
            return pd.DataFrame({x: data_x, y: data_y})

    def convert_to_series(self, data, label=None):
        label = label if label else "Data"
        return pd.DataFrame({label: data})[label]


class CorrelationTestData(TraceData):
    __instance = None

    @staticmethod
    def get_instance():
        if CorrelationTestData.__instance is None:
            CorrelationTestData()
        return CorrelationTestData.__instance

    def __init__(self):
        if CorrelationTestData.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            CorrelationTestData.__instance = self

    def load_data(self, data_file):
        data = np.load(data_file)
        self.traces = (data["traces"]).astype(float)
        self.nr_of_traces, self.nr_of_samples = self.traces.shape
        self.plain_text = data["pt"]

    # def get_traces(self):
    #     return self.traces

    # def get_plain_text(self):
    #     return self.plain_text

    # def get_nr_of_traces(self):
    #     return self.nr_of_traces

    # def get_nr_of_samples(self):
    #     return self.nr_of_samples
