from leak_calc import TVLA, CorrelationTest, TestType
from core.plotter import Plotter


class LeakageDetectionFramework:
    def __init__(self, test_type=None, tester=None):
        if tester:
            self.tester = tester
            self.test_type = TestType.personalised_test
        else:
            self.test_type = test_type if test_type else TestType.t_test
            self.tester = self.__get_tester_based_on_type()

    def __get_tester_based_on_type(self):
        print(self.test_type)
        if self.test_type == TestType.t_test:
            return TVLA()
        elif self.test_type == TestType.correlation_test:
            return CorrelationTest()
        else:
            return None

    def load_data(self, **data_file):
        self.tester.data_loader.load_data(**data_file)

    def execute_test(self, **params):
        return self.tester.execute_test(**params)

    def trace_data(self):
        return self.tester.data_loader

    def plotter(self, style=None):
        return Plotter(style)
