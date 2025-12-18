class SimulationSettings:
    ARRIVAL_INTERVAL_MEAN = 3.0  # Mean time between customer arrivals in minutes
    ARRIVAL_DISTRIBUTION = "exponential"  # Distribution type for arrivals

    SERVICE_TIME_MEAN = 10.0  # Mean service time in minutes
    SERVICE_TIME_STD = 2.0  # Standard deviation for service time (if using normal distribution)
    SERVICE_TIME_DISTRIBUTION = "normal"  # Distribution type for service times

    NUMBER_OF_COUNTERS = 3  # Number of service counters
    SIMULATION_TIME = 480
    WARMUP_TIME = 20

    RANDOM_SEED = 36 # Seed for random number generation

    ENABLE_REALTIME_MONITORING = True  # Enable or disable real-time monitoring
    ENABLE_REALTIME_MONITOR = True  # Alias for ENABLE_REALTIME_MONITORING (for monitor compatibility)
    SNAPSHOT_INTERVAL = 1.0  # Interval for periodic snapshots in minutes
    EXPORT_FORMAT = ["csv", "json"]  # Formats for exporting results