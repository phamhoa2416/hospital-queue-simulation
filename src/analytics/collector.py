import numpy as np
from typing import List


class StatisticsCollector:
    def __init__(self):
        self.data = {
            'waiting_times': [],
            'service_times': [],
            'time_in_system': [],
            'queue_lengths': [],
            'counter_utilization': []
        }

    def collect_from_patients(self, patients):
        for patient in patients:
            if patient.waiting_time is not None:
                self.data['waiting_times'].append(patient.waiting_time)
            if patient.service_time is not None:
                self.data['service_times'].append(patient.service_time)
            if patient.total_time_in_system is not None:
                self.data['time_in_system'].append(patient.total_time_in_system)

    def collect_from_counters(self, counters, total_simulation_time):
        for counter in counters:
            utilization = counter.calculate_utilization(total_simulation_time)
            self.data['counter_utilization'].append({
                'counter_id': counter.id,
                'utilization': utilization,
                'patients_served': counter.total_patients_served,
                'total_busy_time': counter.total_busy_time
            })
    
    def collect_from_queue_snapshots(self, queue_snapshots):
        if queue_snapshots:
            self.data['queue_lengths'] = [snapshot['queue_length'] 
                                         for snapshot in queue_snapshots]
    
    def get_data_summary(self) -> dict:
        summary = {}
        
        for key, values in self.data.items():
            if values and isinstance(values[0], (int, float)):
                arr = np.array(values)
                summary[key] = {
                    'count': len(arr),
                    'mean': float(np.mean(arr)),
                    'std': float(np.std(arr)),
                    'min': float(np.min(arr)),
                    'max': float(np.max(arr)),
                    'median': float(np.median(arr))
                }
            else:
                summary[key] = {
                    'count': len(values),
                    'type': 'non_numeric'
                }
        
        return summary
    
    def clear(self):
        for key in self.data:
            self.data[key] = []

