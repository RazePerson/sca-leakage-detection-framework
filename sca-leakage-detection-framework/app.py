from core import LeakageDetectionFramework
from math_util import MathUtil

class App():

    def start_app(self):
        ldf = LeakageDetectionFramework()
        ldf.load_data('../traces/REASSURE_power_Unprotected_AES_fixed_vs_random_Exp1.npz')
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
        print(math_util.mean([[1,2,3],[0,2,5]]))

app = App()
# app.test_math()
app.start_app()