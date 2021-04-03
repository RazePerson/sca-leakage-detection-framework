import pandas as pd


class TraceData:
    __instance = None

    @staticmethod
    def get_instance():
        if TraceData.__instance is None:
            TraceData()
        return TraceData.__instance

    def __init__(self):
        if TraceData.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            TraceData.__instance = self

    def initialise(self, data):
        self.data = data
        self.extract_dataset_components()

    def extract_dataset_components(self):
        self.traces = (self.data["traces"]).astype(float)
        self.flag = self.data["flag"]
        self.plain_text = self.data["pt"]
        self.nr_of_traces, self.nr_of_samples = self.traces.shape

    def get_all_traces(self):
        return self.traces[0, :]

    def get_fixed_traces(self):
        fixed_trace_index = self.flag == 1
        return self.traces[fixed_trace_index[:, 0], :]

    def get_random_traces(self):
        random_trace_index = self.flag == 0
        return self.traces[random_trace_index[:, 0], :]

    def convert_t_statistic_to_data_frame(self, data):
        return self.convert_to_data_frame(data_y=data, x="Time Samples", y="T-Statistic")

    def convert_to_data_frame(self, data_y, data_x=None, x=None, y=None):
        x = x if x else "Length"
        y = y if y else "Data"
        if not data_x:
            return pd.DataFrame({x: range(0, len(data_y)), y: data_y})
        else:
            return pd.DataFrame({x: data_x, y: data_y})