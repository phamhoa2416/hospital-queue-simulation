import sys
import os
from datetime import datetime
from contextlib import contextmanager

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import SimulationSettings
from simulation.environment import SimulationEnvironment
from simulation.monitor import SimulationMonitor
from simulation.process import SimulationProcess
from analytics.analyzer import SimulationAnalyzer
from analytics.visualizer import SimulationVisualizer


class TeeOutput:
    """Class to write output to both console and file"""
    def __init__(self, file_path):
        self.file = open(file_path, 'w', encoding='utf-8')
        self.stdout = sys.stdout
        
    def write(self, text):
        self.stdout.write(text)
        self.file.write(text)
        self.file.flush()
        
    def flush(self):
        self.stdout.flush()
        self.file.flush()
        
    def close(self):
        self.file.close()


@contextmanager
def log_to_file(file_path):
    tee = TeeOutput(file_path)
    original_stdout = sys.stdout
    sys.stdout = tee
    try:
        yield tee
    finally:
        sys.stdout = original_stdout
        tee.close()


def run_simulation(settings=None):
    if settings is None:
        settings = SimulationSettings()
    
    print("=" * 60)
    print("HOSPITAL QUEUE SIMULATION")
    print("=" * 60)
    print(f"Simulation Parameters:")
    print(f"  - Number of counters: {settings.NUMBER_OF_COUNTERS}")
    print(f"  - Simulation time: {settings.SIMULATION_TIME} minutes")
    print(f"  - Warmup time: {settings.WARMUP_TIME} minutes")
    print(f"  - Arrival interval mean: {settings.ARRIVAL_INTERVAL_MEAN} minutes")
    print(f"  - Service time mean: {settings.SERVICE_TIME_MEAN} minutes")
    print(f"  - Random seed: {settings.RANDOM_SEED}")
    print("=" * 60)
    print("\nStarting simulation...\n")

    sim_env = SimulationEnvironment(settings)
    monitor = SimulationMonitor(sim_env, settings)
    process = SimulationProcess(sim_env, settings, monitor)

    sim_env.env.process(process.arrival_process())

    if hasattr(settings, 'SNAPSHOT_INTERVAL') and settings.SNAPSHOT_INTERVAL > 0:
        sim_env.env.process(monitor.periodic_snapshot())

    try:
        sim_env.env.run(until=settings.SIMULATION_TIME)
        print(f"\nSimulation completed at time: {sim_env.env.now:.2f} minutes")
    except Exception as e:
        print(f"\nError during simulation: {e}")
        raise

    for patient in sim_env.patients:
        if patient.service_end_time is None and patient.service_start_time is not None:
            patient.service_end_time = sim_env.env.now
            patient.calculate_metrics()
        elif patient.service_end_time is None:
            pass

    analyzer = SimulationAnalyzer(
        patients=sim_env.patients,
        counters=sim_env.counter_list,
        total_simulation_time=settings.SIMULATION_TIME
    )

    visualizer = SimulationVisualizer(analyzer, output_dir="output")
    
    return sim_env, monitor, analyzer, visualizer


def main():
    settings = SimulationSettings()

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"simulation_log_{timestamp}.txt")

    with log_to_file(log_file_path):
        print(f"Log file: {log_file_path}\n")
        print("=" * 60)
        
        try:
            sim_env, monitor, analyzer, visualizer = run_simulation(settings)

            print("\n")
            analyzer.print_summary()

            print("\nGenerating visualizations...")
            visualizer.generate_all()

            print("\n" + "=" * 60)
            print("SIMULATION SUMMARY")
            print("=" * 60)

            print("\nCounter Details:")
            for counter in sim_env.counter_list:
                utilization = counter.calculate_utilization(settings.SIMULATION_TIME)
                print(f"  Counter {counter.id}: "
                      f"{counter.total_patients_served} patients served, "
                      f"{utilization:.2f}% utilization")
            
            print("\n" + "=" * 60)
            print("Simulation completed successfully!")
            print("=" * 60)
            print(f"\nLog saved to: {log_file_path}")
            
        except KeyboardInterrupt:
            print("\n\nSimulation interrupted by user")
            print(f"\nPartial log saved to: {log_file_path}")
            sys.exit(1)
        except Exception as e:
            print(f"\n\nError: {e}")
            import traceback
            traceback.print_exc()
            print(f"\nError log saved to: {log_file_path}")
            sys.exit(1)


if __name__ == "__main__":
    main()

