import numpy as np
from typing import List, Dict


class SimulationAnalyzer:
    def __init__(self, patients: List, counters: List, total_simulation_time: float):
        self.patients = patients
        self.counters = counters
        self.total_simulation_time = total_simulation_time

        self.waiting_times = [p.waiting_time for p in self.patients if p.waiting_time is not None]

    def get_essential_report(self) -> Dict:
        total_arrivals = len(self.patients)

        total_served = len([p for p in self.patients if p.service_end_time is not None])

        total_remaining = total_arrivals - total_served

        avg_wait = np.mean(self.waiting_times) if self.waiting_times else 0.0
        max_wait = np.max(self.waiting_times) if self.waiting_times else 0.0

        throughput = total_served / self.total_simulation_time if self.total_simulation_time > 0 else 0.0

        counter_utilization = [
            counter.calculate_utilization(self.total_simulation_time)
            for counter in self.counters
        ]
        avg_utilization = np.mean(counter_utilization) if counter_utilization else 0.0

        return {
            "total_arrivals": total_arrivals,
            "total_served": total_served,
            "total_remaining": total_remaining,
            "average_waiting_time": float(avg_wait),
            "max_waiting_time": float(max_wait),
            "throughput": float(throughput),
            "average_utilization": float(avg_utilization)
        }

    def print_summary(self):
        report = self.get_essential_report()
        print("\n" + "=" * 40)
        print("QUEUE SYSTEM STATISTICS REPORT")
        print("=" * 40)
        print(f"1. Total arrivals:                {report['total_arrivals']} patients")
        print(f"2. Total patients served:          {report['total_served']} patients")
        print(f"3. Remaining patients:             {report['total_remaining']} patients")
        print(f"4. Average waiting time:           {report['average_waiting_time']:.2f} minutes")
        print(f"5. Maximum waiting time:           {report['max_waiting_time']:.2f} minutes")
        print(f"6. Throughput:                     {report['throughput']:.2f} patients/min")
        print(f"7. Average service efficiency:     {report['average_utilization']:.2f}%")
        print("=" * 40)

