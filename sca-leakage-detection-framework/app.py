from core import LeakageDetectionFramework
from leak_calc import MathUtil
from data import TVLAData


class App:
    def __init__(self):
        self.ldf = LeakageDetectionFramework()
        self.ldf.load_data("../traces/REASSURE_power_Unprotected_AES_fixed_vs_random_Exp1.npz")

    def old_test(self):
        ldf = LeakageDetectionFramework()
        ldf.load_data("../traces/REASSURE_power_Unprotected_AES_fixed_vs_random_Exp1.npz")
        ldf.extract_dataset_components()

        ldf.welch_t_statistic()
        stat_range = range(0, 13900)
        threshold = 4.5
        ldf.indices_of_leaky_samples(stat_range, threshold)
        ldf.create_default_plots()

        stat_range = range(0, 1000)
        threshold = 4.5
        ldf.indices_of_leaky_samples(stat_range, threshold)
        ldf.create_default_plots()

        ldf.plot()
        # print(ldf.t_statistic)

    def test_leakage(self):
        t_test_data = TVLAData.get_instance()
        stat_range = range(0, 13900)
        threshold = 4.5
        t_statistic = self.ldf.calculate_t_statistic()
        leakage = self.ldf.indices_of_leaky_samples(t_statistic, stat_range, threshold)

        print(leakage.sum())
        print(t_statistic)
        plotter = self.ldf.plotter()
        print(t_statistic.shape)
        t_stat_data_frame = t_test_data.convert_t_statistic_to_data_frame(t_statistic)
        traces = t_test_data.convert_to_data_frame(t_test_data.get_all_traces())
        coord = ((12, 40), (30, 59), (2500, 23), (5760, 81), (6000, 10))
        plotter.create_line_plot(t_stat_data_frame).show_threshold(threshold).highlight_points(coord).create_line_plot(
            t_stat_data_frame
        ).create_line_plot(traces).plot()

    def test_math(self):
        math_util = MathUtil()
        mean = math_util.mean(self.ldf.t_test_data.get_every_fixed_trace())
        print(mean)


app = App()
app.test_leakage()
# app.test_math()
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