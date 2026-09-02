"""Interfaces for future system simulations."""

from dataclasses import dataclass, field
from typing import Protocol

from digital_twin.monitoring import SystemSnapshot


@dataclass(frozen=True)
class SimulationScenario:
    """A named set of changes to explore in a simulated system."""

    name: str
    description: str = ""


@dataclass(frozen=True)
class SimulationResult:
    """The output of running a simulation scenario."""

    scenario: SimulationScenario
    snapshots: tuple[SystemSnapshot, ...] = field(default_factory=tuple)


class SimulationEngine(Protocol):
    """Interface for running controlled what-if scenarios."""

    def run(self, scenario: SimulationScenario) -> SimulationResult:
        """Run a scenario and return its simulated observations."""

        ...