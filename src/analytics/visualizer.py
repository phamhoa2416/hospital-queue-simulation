import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from typing import Optional


class SimulationVisualizer:
    def __init__(self, analyzer, output_dir: str = "visualize"):
        self.analyzer = analyzer
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10

    def plot_waiting_time(self, save_path: Optional[str] = None):
        if len(self.analyzer.waiting_times) == 0:
            return

        plt.figure(figsize=(10, 5))
        sns.histplot(self.analyzer.waiting_times, kde=True, color='steelblue', bins=20)

        avg_wait = np.mean(self.analyzer.waiting_times)
        plt.axvline(avg_wait, color='red', linestyle='--', label=f'Average: {avg_wait:.2f} min')

        plt.title('Patient Waiting Time Distribution', fontweight='bold')
        plt.xlabel('Waiting time (minutes)')
        plt.ylabel('Number of patients')
        plt.legend()

        path = save_path or os.path.join(self.output_dir, 'waiting_time.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_counter_performance(self, save_path: Optional[str] = None):
        report = self.analyzer.get_essential_report()
        counter_ids = [f"Counter {i + 1}" for i in range(len(self.analyzer.counters))]
        utilization = [c.calculate_utilization(self.analyzer.total_simulation_time) for c in self.analyzer.counters]

        fig, ax1 = plt.subplots(figsize=(10, 5))

        bars = ax1.bar(counter_ids, utilization, color='skyblue', alpha=0.7)
        ax1.set_ylabel('Performance (%)', fontsize=12)
        ax1.set_ylim(0, 100)

        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.1f}%', ha='center', va='bottom')

        plt.title('Counter Service Performance', fontweight='bold')

        path = save_path or os.path.join(self.output_dir, 'counter_performance.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_summary_dashboard(self, save_path: Optional[str] = None):
        report = self.analyzer.get_essential_report()

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis('off')

        stats_text = (
            f"SIMULATION RESULTS SUMMARY\n"
            f"{'=' * 30}\n"
            f"- Total arrivals: {report['total_arrivals']}\n"
            f"- Total patients served: {report['total_served']}\n"
            f"- Remaining patients: {report['total_remaining']}\n"
            f"- Average waiting time: {report['average_waiting_time']:.2f} minutes\n"
            f"- Maximum waiting time: {report['max_waiting_time']:.2f} minutes\n"
            f"- Throughput: {report['throughput']:.2f} patients/min\n"
            f"- System efficiency: {report['average_utilization']:.2f}%"
        )

        ax.text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
                va='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        path = save_path or os.path.join(self.output_dir, 'summary_report.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def generate_all(self):
        self.plot_waiting_time()
        self.plot_counter_performance()
        self.plot_summary_dashboard()
        print(f"Plots exported to directory: {self.output_dir}")

