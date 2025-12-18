class Patient:
    _id_counter = 0

    def __init__(self):
        Patient._id_counter += 1
        self.id = Patient._id_counter

        self.arrival_time = None
        self.queue_join_time = None
        self.service_start_time = None
        self.service_end_time = None

        self.waiting_time = None
        self.service_time = None
        self.total_time_in_system = None

        self.assigned_counter = None

    def calculate_metrics(self):
        if self.service_start_time and self.queue_join_time:
            self.waiting_time = self.service_start_time - self.queue_join_time
        if self.service_end_time and self.service_start_time:
            self.service_time = self.service_end_time - self.service_start_time
        if self.service_end_time and self.arrival_time:
            self.total_time_in_system = self.service_end_time - self.arrival_time

    def to_dict(self):
        return {
            "id": self.id,
            "arrival_time": self.arrival_time,
            "waiting_time": self.waiting_time,
            "service_time": self.service_time,
            "total_time_in_system": self.total_time_in_system,
            "counter": self.assigned_counter
        }