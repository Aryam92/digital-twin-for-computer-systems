"""Tests for the Digital Twin simulation engine."""

import unittest
from datetime import datetime

from digital_twin.health import HealthStatus
from digital_twin.monitoring import SystemSnapshot
from digital_twin.simulation import SimulationEngine, SimulationScenario


class TestSimulationEngine(unittest.TestCase):

    def test_critical_scenario(self):
        snapshot = SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=20,
            memory_percent=30,
            disk_percent=30,
            running_processes=100,
            network_sent_bytes=0,
            network_received_bytes=0,
        )

        scenario = SimulationScenario(
            name="Critical Test",
            description="Simulates a critical workload.",
            cpu_percent=95,
            memory_percent=95,
            disk_percent=95,
        )

        engine = SimulationEngine()
        result = engine.run(scenario, snapshot)

        self.assertEqual(result.snapshot.cpu_percent, 95)
        self.assertEqual(result.snapshot.memory_percent, 95)
        self.assertEqual(result.snapshot.disk_percent, 95)
        self.assertEqual(result.health_report.status, HealthStatus.CRITICAL)
        self.assertGreater(len(result.health_report.recommendations), 0)


if __name__ == "__main__":
    unittest.main()