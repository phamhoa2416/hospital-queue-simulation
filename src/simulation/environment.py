import simpy
from models.counter import Counter

class SimulationEnvironment:
    def __init__(self, settings):
        self.settings = settings
        self.env = simpy.Environment()

        self.counters = simpy.Resource(self.env, capacity=settings.NUMBER_OF_COUNTERS)
        self.counter_list = [Counter(i + 1) for i in range(settings.NUMBER_OF_COUNTERS)]

        self.patients = []
        self.queue_length_over_time = []
        self.current_queue_length = 0

    def get_available_counter(self):
        for counter in self.counter_list:
            if not counter.is_busy:
                return counter
        return self.counter_list[0] if self.counter_list else None
