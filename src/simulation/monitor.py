class SimulationMonitor:
    def __init__(self, sim_env, settings):
        self.sim_env = sim_env
        self.env = sim_env.env
        self.settings = settings

        self.queue_snapshots = []
        self.events_log = []

    def record_arrival(self, patient):
        self.events_log.append({
            'time': self.env.now,
            'event': 'arrival',
            'patient_id': patient.id,
            'queue_length': self.sim_env.current_queue_length
        })

        # Check both attribute names for compatibility
        enable_monitor = getattr(self.settings, 'ENABLE_REALTIME_MONITOR', None) or \
                        getattr(self.settings, 'ENABLE_REALTIME_MONITORING', False)
        if enable_monitor:
            print(f"{self.env.now:.2f}: Patient {patient.id} arrived. Queue length: {self.sim_env.current_queue_length}")

    def record_service_start(self, patient, counter):
        self.events_log.append({
            'time': self.env.now,
            'event': 'service_start',
            'patient_id': patient.id,
            'counter_id': counter.id,
            'queue_length': self.sim_env.current_queue_length
        })

    def record_service_end(self, patient, counter):
        self.events_log.append({
            'time': self.env.now,
            'event': 'service_end',
            'patient_id': patient.id,
            'counter_id': counter.id,
            'queue_length': self.sim_env.current_queue_length
        })

    def periodic_snapshot(self):
        while True:
            self.queue_snapshots.append({
                'time': self.env.now,
                'queue_length': self.sim_env.current_queue_length,
                'total_arrivals': len(self.sim_env.patients),
                'total_served': sum(1 for p in self.sim_env.patients if p.service_end_time is not None)
            })

            yield self.env.timeout(self.settings.SNAPSHOT_INTERVAL)