import numpy as np

class RandomGenerator:
    def __init__(self, settings):
        self.settings = settings
        np.random.seed(settings.RANDOM_SEED)

    def get_arrival_time(self):
        if self.settings.ARRIVAL_DISTRIBUTION == "exponential":
            return np.random.exponential(self.settings.ARRIVAL_INTERVAL_MEAN)
        elif self.settings.ARRIVAL_DISTRIBUTION == "uniform":
            low = self.settings.ARRIVAL_INTERVAL_MEAN * 0.5
            high = self.settings.ARRIVAL_INTERVAL_MEAN * 1.5
            return np.random.uniform(low, high)
        else:
            return self.settings.ARRIVAL_INTERVAL_MEAN

    def get_service_time(self):
        if self.settings.SERVICE_TIME_DISTRIBUTION == "normal":
            time = np.random.normal(
                self.settings.SERVICE_TIME_MEAN,
                self.settings.SERVICE_TIME_STD
            )
            return max(0.1, time)
        elif self.settings.SERVICE_TIME_DISTRIBUTION == "exponential":
            return np.random.exponential(self.settings.SERVICE_TIME_MEAN)
        else:
            return self.settings.SERVICE_TIME_MEAN