class TVLAResult:
    def __init__(self, t_statistic, nr_of_leaky_points, leaky_indices, leaky_samples):
        self.t_statistic = t_statistic
        self.nr_of_leaky_points = nr_of_leaky_points
        self.leaky_indices = leaky_indices
        self.leaky_samples = leaky_samples

    def __str__(self):
        return (
            "T-Statistic: "
            + str(self.t_statistic)
            + "\nNr. of leaky points: "
            + str(self.nr_of_leaky_points)
            + "\nLeaky indices: "
            + str(self.leaky_indices)
            + "\nLeaky samples: "
            + str(self.leaky_samples)
        )


class CorrelationTestResult:
    pass
