from leak_calc import MathUtil

class TVLA():
    def __init__(self):
        self.stuff = 0

    def welch_t_statistic(self, data):
        tF_index = self.flag == 1
        tR_index = self.flag == 0

        NF = tF_index.sum()
        NR = tR_index.sum()

        math_util = MathUtil()

        meanF = math_util.mean(self.traces, indices=tF_index)
        meanR = math_util.mean(self.traces, indices=tR_index)
        varF = math_util.variance(self.traces, indices=tF_index)
        varR = math_util.variance(self.traces, indices=tR_index)

        return (meanF - meanR) / np.sqrt(varF / NF + varR / NR)