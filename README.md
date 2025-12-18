# Hospital Queue Simulation System

A discrete-event simulation system for modeling and analyzing patient queue management in a hospital setting. This system simulates patient arrivals, queue management, and service at multiple counters, providing comprehensive statistics and visualizations.

## Features

- **Discrete-Event Simulation**: Built using SimPy for realistic event-driven simulation
- **Multiple Service Counters**: Configurable number of service counters
- **Statistical Analysis**: Comprehensive metrics including waiting times, service times, and system utilization
- **Data Visualization**: Automatic generation of charts and graphs using matplotlib and seaborn
- **Logging System**: Complete simulation logs saved to text files with timestamps
- **Configurable Parameters**: Easy customization of arrival rates, service times, and system configuration

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

The required packages are:
- `simpy` - Discrete-event simulation framework
- `numpy` - Numerical computations
- `pandas` - Data manipulation (optional, for future data export)
- `matplotlib` - Plotting library
- `seaborn` - Statistical visualization

## Project Structure

```
hospital-queue-simulation/
├── src/
│   ├── config/
│   │   └── settings.py          # Simulation configuration parameters
│   ├── models/
│   │   ├── patient.py           # Patient entity model
│   │   └── counter.py           # Service counter model
│   ├── simulation/
│   │   ├── environment.py       # SimPy environment setup
│   │   ├── process.py            # Arrival and service processes
│   │   └── monitor.py           # Event monitoring and logging
│   ├── analytics/
│   │   ├── analyzer.py          # Statistical analysis
│   │   ├── visualizer.py        # Chart generation
│   │   └── collector.py         # Data collection utilities
│   ├── utils/
│   │   └── generator.py         # Random number generation
│   ├── run_simulation.py        # Main simulation runner
│   └── test_simulation.py      # System testing script
├── requirements.txt
└── README.md
```

## Usage

### Running the Simulation

1. **Run the full simulation:**
```bash
cd src
python run_simulation.py
```

This will:
- Execute the simulation with default parameters
- Generate statistical reports
- Create visualization charts
- Save logs to `logs/simulation_log_YYYYMMDD_HHMMSS.txt`
- Save charts to `output/` directory

2. **Test the system:**
```bash
cd src
python test_simulation.py
```

This runs a quick test to verify all components are working correctly.

### Configuration

Edit `src/config/settings.py` to customize simulation parameters:

```python
class SimulationSettings:
    # Arrival parameters
    ARRIVAL_INTERVAL_MEAN = 3.0  # Mean time between arrivals (minutes)
    ARRIVAL_DISTRIBUTION = "exponential"  # Distribution type
    
    # Service parameters
    SERVICE_TIME_MEAN = 10.0  # Mean service time (minutes)
    SERVICE_TIME_STD = 2.0  # Standard deviation for service time
    SERVICE_TIME_DISTRIBUTION = "normal"  # Distribution type
    
    # System configuration
    NUMBER_OF_COUNTERS = 3  # Number of service counters
    SIMULATION_TIME = 480  # Total simulation time (minutes)
    WARMUP_TIME = 20  # Warmup period (minutes)
    
    # Other settings
    RANDOM_SEED = 36  # Random seed for reproducibility
    ENABLE_REALTIME_MONITORING = True  # Enable real-time event logging
    SNAPSHOT_INTERVAL = 1.0  # Queue snapshot interval (minutes)
```

### Customizing Simulation in Code

You can also modify settings programmatically in `run_simulation.py`:

```python
def main():
    settings = SimulationSettings()
    settings.NUMBER_OF_COUNTERS = 5
    settings.SIMULATION_TIME = 240
    settings.ENABLE_REALTIME_MONITORING = False
    # ... run simulation
```

## System Architecture

### Core Components

1. **SimulationEnvironment**
   - Manages the SimPy simulation environment
   - Creates and manages service counters as resources
   - Tracks queue state

2. **SimulationProcess**
   - **Arrival Process**: Generates patients at intervals following specified distribution
   - **Service Process**: Handles patient service at counters

3. **SimulationMonitor**
   - Records all simulation events (arrivals, service starts/ends)
   - Takes periodic snapshots of queue state
   - Logs real-time events (if enabled)

4. **SimulationAnalyzer**
   - Calculates statistical metrics:
     - Total arrivals and patients served
     - Average and maximum waiting times
     - Throughput (patients per minute)
     - Counter utilization rates

5. **SimulationVisualizer**
   - Generates visualization charts:
     - Waiting time distribution
     - Counter performance metrics
     - Summary dashboard

### Simulation Flow

1. **Initialization**: Create environment, counters, and monitoring systems
2. **Arrival Process**: Patients arrive at intervals determined by arrival distribution
3. **Queue Management**: Patients wait for available counter resources
4. **Service Process**: Patients are served at counters for a duration following service time distribution
5. **Data Collection**: All events and metrics are recorded
6. **Analysis**: Statistical analysis is performed on collected data
7. **Visualization**: Charts and reports are generated
8. **Logging**: Complete simulation log is saved to file

## Output

### Log Files

Simulation logs are automatically saved to `logs/` directory with format:
- `simulation_log_YYYYMMDD_HHMMSS.txt`

Logs contain:
- Simulation parameters
- Real-time event logs (if enabled)
- Statistical summary
- Counter utilization details

### Visualization Charts

Charts are saved to `output/` directory:
- `waiting_time.png` - Distribution of patient waiting times
- `counter_performance.png` - Performance metrics for each counter
- `summary_report.png` - Summary dashboard with key statistics

### Console Output

The simulation prints:
- Simulation parameters
- Real-time events (if monitoring enabled)
- Statistical summary report
- Counter details
- Completion status

## Key Metrics

The system calculates and reports:

- **Total Arrivals**: Number of patients that arrived during simulation
- **Total Served**: Number of patients that completed service
- **Remaining Patients**: Patients still in queue or being served at simulation end
- **Average Waiting Time**: Mean time patients spent waiting in queue
- **Maximum Waiting Time**: Longest waiting time experienced
- **Throughput**: Rate of patients served per minute
- **Counter Utilization**: Percentage of time each counter was busy

## Distribution Types

### Arrival Distribution
- **Exponential**: Inter-arrival times follow exponential distribution
- **Uniform**: Inter-arrival times follow uniform distribution

### Service Time Distribution
- **Normal**: Service times follow normal distribution with mean and standard deviation
- **Exponential**: Service times follow exponential distribution

## Example Output

```
============================================================
HOSPITAL QUEUE SIMULATION
============================================================
Simulation Parameters:
  - Number of counters: 3
  - Simulation time: 480 minutes
  - Arrival interval mean: 3.0 minutes
  - Service time mean: 10.0 minutes
============================================================

============================================================
QUEUE SYSTEM STATISTICS REPORT
============================================================
1. Total arrivals:                160 patients
2. Total patients served:          145 patients
3. Remaining patients:             15 patients
4. Average waiting time:           5.23 minutes
5. Maximum waiting time:           18.45 minutes
6. Throughput:                     0.30 patients/min
7. Average service efficiency:     78.50%
============================================================
```

