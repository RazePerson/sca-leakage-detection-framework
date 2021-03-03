from core import LeakageDetectionFramework
from leak_calc import MathUtil
from visualisation import (SeabornPlotter, DefaultPlotter)


class App:
    def __init__(self):
        self.ldf = LeakageDetectionFramework()
        self.ldf.load_data(
            "../traces/REASSURE_power_Unprotected_AES_fixed_vs_random_Exp1.npz"
        )
        self.ldf.extract_dataset_components()

    def old_test(self):
        ldf = LeakageDetectionFramework()
        ldf.load_data(
            "../traces/REASSURE_power_Unprotected_AES_fixed_vs_random_Exp1.npz"
        )
        ldf.extract_dataset_components()

        ldf.welch_t_statistic()
        stat_range = range(0, 13900)
        threshold = 4.5
        ldf.calculate_leakage(stat_range, threshold)
        ldf.create_default_plots()

        stat_range = range(0, 1000)
        threshold = 4.5
        ldf.calculate_leakage(stat_range, threshold)
        ldf.create_default_plots()

        ldf.plot()
        # print(ldf.t_statistic)

    def test_math(self):
        math_util = MathUtil()
        
        meanF = math_util.mean(self.ldf.traces, indices=tF_index)
        print(meanF)


app = App()
print(app.ldf.traces.shape)
app.test_math()
# app.test_math()
# app.old_test()
# snsp = SeabornPlotter()
# print(app.ldf.traces[0, :])
# math_util = MathUtil()
# snsp.create_plot_line(math_util.mean(app.ldf.traces))

# defp = DefaultPlotter()
# defp.create_power_trace_plot(app.ldf)
# snsp.plot()
# snsp.create_plot(app.ldf.traces[0, :])
# snsp.plot()