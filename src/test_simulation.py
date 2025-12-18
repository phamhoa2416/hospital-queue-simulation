import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import SimulationSettings
from simulation.environment import SimulationEnvironment
from simulation.monitor import SimulationMonitor
from simulation.process import SimulationProcess
from analytics.analyzer import SimulationAnalyzer
from analytics.visualizer import SimulationVisualizer


def test_simulation():
    print("=" * 60)
    print("TESTING SIMULATION SYSTEM")
    print("=" * 60)

    settings = SimulationSettings()
    settings.SIMULATION_TIME = 30  # Short test run
    settings.WARMUP_TIME = 5
    settings.ENABLE_REALTIME_MONITORING = False  # Disable verbose output for test
    
    print("\nTest Parameters:")
    print(f"  - Simulation time: {settings.SIMULATION_TIME} minutes")
    print(f"  - Number of counters: {settings.NUMBER_OF_COUNTERS}")
    print(f"  - Random seed: {settings.RANDOM_SEED}")
    
    try:
        print("\n[Test 1] Initializing components...")
        sim_env = SimulationEnvironment(settings)
        monitor = SimulationMonitor(sim_env, settings)
        process = SimulationProcess(sim_env, settings, monitor)
        print("✓ All components initialized successfully")

        print("\n[Test 2] Starting simulation processes...")
        sim_env.env.process(process.arrival_process())
        if hasattr(settings, 'SNAPSHOT_INTERVAL') and settings.SNAPSHOT_INTERVAL > 0:
            sim_env.env.process(monitor.periodic_snapshot())
        print("✓ Simulation processes started")

        print("\n[Test 3] Running simulation...")
        sim_env.env.run(until=settings.SIMULATION_TIME)
        print(f"✓ Simulation completed at time: {sim_env.env.now:.2f} minutes")

        print("\n[Test 4] Verifying data collection...")
        assert len(sim_env.patients) > 0, "No patients generated"
        assert len(monitor.events_log) > 0, "No events logged"
        print(f"✓ Generated {len(sim_env.patients)} patients")
        print(f"✓ Logged {len(monitor.events_log)} events")
        print(f"✓ Collected {len(monitor.queue_snapshots)} queue snapshots")

        print("\n[Test 5] Testing analyzer...")
        analyzer = SimulationAnalyzer(
            patients=sim_env.patients,
            counters=sim_env.counter_list,
            total_simulation_time=settings.SIMULATION_TIME
        )
        report = analyzer.get_essential_report()
        assert 'total_arrivals' in report, "Missing total_arrivals in report"
        assert 'total_served' in report, "Missing total_served in report"
        print("✓ Analyzer working correctly")
        print(f"  - Total arrivals: {report['total_arrivals']}")
        print(f"  - Total served: {report['total_served']}")

        print("\n[Test 6] Testing visualizer...")
        visualizer = SimulationVisualizer(analyzer, output_dir="test_output")
        print("✓ Visualizer initialized successfully")

        print("\n[Test 7] Verifying counter statistics...")
        for counter in sim_env.counter_list:
            utilization = counter.calculate_utilization(settings.SIMULATION_TIME)
            assert 0 <= utilization <= 100, f"Invalid utilization: {utilization}"
            print(f"  - Counter {counter.id}: {utilization:.2f}% utilization, "
                  f"{counter.total_patients_served} patients served")
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nSimulation system is working correctly.")
        print("You can now run the full simulation using: python run_simulation.py")
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_simulation()
    sys.exit(0 if success else 1)

