"""What-if simulation engine for the Digital Twin."""

from dataclasses import dataclass, field

from digital_twin.health import HealthReport, SystemHealthAnalyzer
from digital_twin.monitoring import SystemSnapshot


@dataclass(frozen=True)
class SimulationScenario:
    """A set of changes to test on a simulated system."""

    name: str
    description: str = ""
    cpu_percent: float | None = None
    memory_percent: float | None = None
    disk_percent: float | None = None


@dataclass(frozen=True)
class SimulationResult:
    """The result of running a what-if scenario."""

    scenario: SimulationScenario
    snapshot: SystemSnapshot
    health_report: HealthReport


class SimulationEngine:
    """Runs what-if scenarios without changing the real system."""

    def __init__(self) -> None:
        self.analyzer = SystemHealthAnalyzer()

    def run(
        self,
        scenario: SimulationScenario,
        current_snapshot: SystemSnapshot,
    ) -> SimulationResult:

        simulated_snapshot = SystemSnapshot(
            timestamp=current_snapshot.timestamp,
            cpu_percent=(
                scenario.cpu_percent
                if scenario.cpu_percent is not None
                else current_snapshot.cpu_percent
            ),
            memory_percent=(
                scenario.memory_percent
                if scenario.memory_percent is not None
                else current_snapshot.memory_percent
            ),
            disk_percent=(
                scenario.disk_percent
                if scenario.disk_percent is not None
                else current_snapshot.disk_percent
            ),
            network_sent_bytes=current_snapshot.network_sent_bytes,
            network_received_bytes=current_snapshot.network_received_bytes,
          running_processes=(
    current_snapshot.running_processes
    if scenario.name != "Normal Workload"
    else 100
),
        )

        health_report = self.analyzer.analyze(simulated_snapshot)

        return SimulationResult(
            scenario=scenario,
            snapshot=simulated_snapshot,
            health_report=health_report,
        )