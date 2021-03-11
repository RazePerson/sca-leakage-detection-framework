from core import LeakageDetectionFramework
from leak_calc import MathUtil


class App:
    def __init__(self):
        self.ldf = LeakageDetectionFramework()
        self.ldf.load_data(
            "../traces/REASSURE_power_Unprotected_AES_fixed_vs_random_Exp1.npz"
        )

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

    def test_leakage(self):
        stat_range = range(0, 13900)
        threshold = 4.5
        t_statistic = self.ldf.calculate_t_statistic()
        leakage = self.ldf.calculate_leakage(t_statistic, stat_range, threshold)

        print(leakage.sum())
        print(t_statistic)
        plotter = self.ldf.plotter()
        t_stat_data_frame = self.ldf.convert_t_statistic_to_data_frame(t_statistic)
        coord = ((12, 40), (30, 59), (2500, 23), (5760, 81), (6000, 10))
        plotter.subplot(1, 2).create_plot(t_stat_data_frame).show_threshold(threshold).mark_points(
            coord
        ).create_plot(t_stat_data_frame).plot()

    def test_math(self):
        math_util = MathUtil()
        mean = math_util.mean(self.ldf.trace_data.get_fixed_traces())
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