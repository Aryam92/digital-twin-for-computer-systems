"""Main application coordinator."""

from .dashboard.app import Dashboard
from .health.analyzer import SystemHealthAnalyzer
from .logging.logger import get_logger
from .monitoring.system_monitor import SystemMonitor
from .simulation import SimulationEngine, SimulationScenario


def main() -> None:
    logger = get_logger(__name__)

    monitor = SystemMonitor()
    analyzer = SystemHealthAnalyzer()
    dashboard = Dashboard()

    # Collect and analyze real system data.
    snapshot = monitor.collect_snapshot()
    report = analyzer.analyze(snapshot)

    # Display the current system state.
    dashboard.render(snapshot, report)

    # Run what-if simulations.
    simulator = SimulationEngine()

    scenarios = [
        SimulationScenario(
            name="Normal Workload",
            description="A normal everyday workload.",
            cpu_percent=50,
            memory_percent=50,
            disk_percent=50,
        ),
        SimulationScenario(
            name="Heavy Workload",
            description="A demanding workload with higher resource usage.",
            cpu_percent=80,
            memory_percent=85,
            disk_percent=75,
        ),
        SimulationScenario(
            name="Critical Workload",
            description="A highly stressed system condition.",
            cpu_percent=95,
            memory_percent=92,
            disk_percent=95,
        ),
    ]

    print()
    print("=" * 60)
    print("              WHAT-IF SIMULATION")
    print("=" * 60)

    for scenario in scenarios:
        result = simulator.run(scenario, snapshot)

        print()
        print(f"Scenario: {scenario.name}")
        print(f"Description: {scenario.description}")
        print(f"Simulated CPU: {result.snapshot.cpu_percent}%")
        print(f"Simulated Memory: {result.snapshot.memory_percent}%")
        print(f"Simulated Disk: {result.snapshot.disk_percent}%")
        print(f"Predicted Health: {result.health_report.score}/100")
        print(
            f"Predicted Status: "
            f"{result.health_report.status.value.upper()}"
        )

        if result.health_report.messages:
            print("Predicted Alerts:")
            for message in result.health_report.messages:
                print(f"  ⚠️ {message}")

        if result.health_report.recommendations:
            print("Predicted Recommendations:")
            for recommendation in result.health_report.recommendations:
                print(f"  → {recommendation}")

        print("-" * 60)

    logger.info("Digital Twin monitoring cycle completed.")


if __name__ == "__main__":
    main()