from models.patient import Patient
from utils.generator import RandomGenerator

class SimulationProcess:
    def __init__(self, sim_env, settings, monitor):
        self.sim_env = sim_env
        self.env = sim_env.env
        self.settings = settings
        self.monitor = monitor
        self.random_generator = RandomGenerator(settings)

    def arrival_process(self):
        while True:
            patient = Patient()
            patient.arrival_time = self.env.now
            patient.queue_join_time = self.env.now

            self.sim_env.patients.append(patient)
            self.sim_env.current_queue_length += 1

            self.monitor.record_arrival(patient)
            self.env.process(self.service_process(patient))
            inter_arrival_time = self.random_generator.get_arrival_time()
            yield self.env.timeout(inter_arrival_time)

    def service_process(self, patient):
        # Wait for an available counter-resource
        with self.sim_env.counters.request() as request:
            yield request

            # Patient has left the queue and is now being served
            self.sim_env.current_queue_length -= 1
            
            # Get an available counter and start service
            counter = self.sim_env.get_available_counter()
            if counter:
                # Use Counter's start_service method to properly track metrics
                counter.start_service(patient, self.env.now)
                patient.service_start_time = self.env.now
                self.monitor.record_service_start(patient, counter)

                # Generate service time and wait
                service_time = self.random_generator.get_service_time()
                yield self.env.timeout(service_time)

                # Service completed - update patient metrics
                patient.service_end_time = self.env.now
                patient.calculate_metrics()
                
                # Use Counter's end_service method to properly track metrics
                counter.end_service(self.env.now)
                self.monitor.record_service_end(patient, counter)
            else:
                patient.service_start_time = self.env.now
                patient.service_end_time = self.env.now
                patient.calculate_metrics()