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

    def load_data(self, data_file):
        self.tester.data_loader.load_data(data_file)

    def execute_test(self, t_stat_range=None, threshold=None, folds=None, byte_to_focus=None):
        if self.test_type == TestType.t_test:
            return self.tester.execute_test(t_stat_range=t_stat_range, threshold=threshold)
        elif self.test_type == TestType.correlation_test:
            return self.tester.execute_test(folds=folds, byte_to_focus=byte_to_focus)
        elif self.test_type == TestType.personalised_test:
            return self.tester.execute_test()
        else:
            return None

    def trace_data(self):
        return self.tester.data_loader

    def plotter(self, style=None):
        return Plotter(style)
