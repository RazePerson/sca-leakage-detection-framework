import pandas as pd
import numpy as np


class TraceData:
    def load_data(self, data_files):
        pass

    def first_data_file(self, **data_files):
        return list(data_files.items())[0][1]


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

    def load_data(self, **data_files):
        data = np.load(self.first_data_file(**data_files))
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

    def load_data(self, **data_files):
        data = np.load(self.first_data_file(**data_files))
        self.traces = (data["traces"]).astype(float)
        print("Trace shape: [%.0f][%.0f]" % (len(self.traces), (len(self.traces[0]))))
        self.nr_of_traces, self.nr_of_samples = self.traces.shape
        self.plain_text = data["pt"]


class SNRTestData(TraceData):
    __instance = None

    @staticmethod
    def get_instance():
        if SNRTestData.__instance is None:
            SNRTestData()
        return SNRTestData.__instance

    def __init__(self):
        if SNRTestData.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            SNRTestData.__instance = self

    def load_data(self, **data_files):
        for key, value in data_files.items():
            if key == "trace_data":
                self.__load_trace_data(value)
            elif key == "plaintext":
                self.__load_plaintext(value)
            else:
                raise NameError('Wrong parameter name was given. Please use the names "trace_data" and "plaintext" for the data files.')

    def __load_trace_data(self, trace_data):
        self.traces = np.load(trace_data)
        self.nr_of_traces = len(self.traces)
        self.nr_of_samples = len(self.traces[0])

    def __load_plaintext(self, plaintext):
        self.plaintext = np.zeros(shape=(self.number_of_traces, 16))

        with open(plaintext) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        self.plaintext = np.array([bytearray.fromhex(c) for c in content])
