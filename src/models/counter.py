class Counter:
    def __init__(self, counter_id):
        self.id = counter_id
        self.total_patients_served = 0
        self.total_busy_time = 0.0
        self.total_idle_time = 0.0

        self.is_busy = False
        self.current_patient = None
        self.service_start_time = None

    def start_service(self, patient, current_time):
        self.is_busy = True
        self.current_patient = patient
        self.service_start_time = current_time
        patient.assigned_counter = self.id

    def end_service(self, current_time):
        if self.service_start_time:
            duration = current_time - self.service_start_time
            self.total_busy_time += duration
            self.total_patients_served += 1

        self.is_busy = False
        self.current_patient = None
        self.service_start_time = None

    def calculate_utilization(self, total_time):
        if total_time > 0:
            return (self.total_busy_time / total_time) * 100.0
        return 0.0