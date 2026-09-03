"""Tests for the Digital Twin simulation engine."""

import unittest
from datetime import datetime

from digital_twin.health import HealthStatus
from digital_twin.monitoring import SystemSnapshot
from digital_twin.simulation import SimulationEngine, SimulationScenario


class TestSimulationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SimulationEngine()

        self.snapshot = SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=30,
            memory_percent=40,
            disk_percent=30,
            running_processes=100,
            network_sent_bytes=0,
            network_received_bytes=0,
        )

    def test_normal_scenario(self):
        scenario = SimulationScenario(
            name="Normal",
            cpu_percent=50,
            memory_percent=50,
            disk_percent=50,
        )

        result = self.engine.run(scenario, self.snapshot)

        self.assertEqual(result.health_report.status, HealthStatus.HEALTHY)

    def test_heavy_scenario(self):
        scenario = SimulationScenario(
            name="Heavy",
            cpu_percent=80,
            memory_percent=85,
            disk_percent=75,
        )

        result = self.engine.run(scenario, self.snapshot)

        self.assertEqual(result.health_report.status, HealthStatus.WARNING)

    def test_critical_scenario(self):
        scenario = SimulationScenario(
            name="Critical",
            cpu_percent=95,
            memory_percent=92,
            disk_percent=95,
        )

        result = self.engine.run(scenario, self.snapshot)

        self.assertEqual(result.health_report.status, HealthStatus.CRITICAL)

    def test_simulation_does_not_modify_real_snapshot(self):
        scenario = SimulationScenario(
            name="Critical",
            cpu_percent=95,
            memory_percent=95,
            disk_percent=95,
        )

        result = self.engine.run(scenario, self.snapshot)

        self.assertEqual(self.snapshot.cpu_percent, 30)
        self.assertEqual(self.snapshot.memory_percent, 40)
        self.assertEqual(self.snapshot.disk_percent, 30)

        self.assertEqual(result.snapshot.cpu_percent, 95)
        self.assertEqual(result.snapshot.memory_percent, 95)
        self.assertEqual(result.snapshot.disk_percent, 95)


if __name__ == "__main__":
    unittest.main()