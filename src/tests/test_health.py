"""Tests for the Digital Twin health analyzer."""

import unittest
from datetime import datetime

from digital_twin.health import HealthStatus, SystemHealthAnalyzer
from digital_twin.monitoring import SystemSnapshot


def make_snapshot(
    cpu=30,
    memory=40,
    disk=30,
    processes=100,
):
    return SystemSnapshot(
        timestamp=datetime.now(),
        cpu_percent=cpu,
        memory_percent=memory,
        disk_percent=disk,
        running_processes=processes,
        network_sent_bytes=0,
        network_received_bytes=0,
    )


class TestSystemHealthAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SystemHealthAnalyzer()

    def test_healthy_system(self):
        report = self.analyzer.analyze(make_snapshot())

        self.assertEqual(report.status, HealthStatus.HEALTHY)
        self.assertEqual(report.score, 100)
        self.assertEqual(report.anomalies, ())

    def test_warning_system(self):
        report = self.analyzer.analyze(
            make_snapshot(
                cpu=80,
                memory=85,
                disk=75,
                processes=100,
            )
        )

        self.assertEqual(report.status, HealthStatus.WARNING)
        self.assertLess(report.score, 80)
        self.assertGreaterEqual(report.score, 60)

    def test_critical_system(self):
        report = self.analyzer.analyze(
            make_snapshot(
                cpu=95,
                memory=95,
                disk=95,
                processes=250,
            )
        )

        self.assertEqual(report.status, HealthStatus.CRITICAL)
        self.assertLess(report.score, 60)
        self.assertGreater(len(report.anomalies), 0)

    def test_critical_memory(self):
        report = self.analyzer.analyze(
            make_snapshot(memory=95)
        )

        self.assertIn("Critical memory usage.", report.messages)
        self.assertTrue(any("Memory" in item for item in report.anomalies))

    def test_critical_disk(self):
        report = self.analyzer.analyze(
            make_snapshot(disk=95)
        )

        self.assertIn("Critical disk usage.", report.messages)
        self.assertTrue(any("Disk" in item for item in report.anomalies))

    def test_high_process_count(self):
        report = self.analyzer.analyze(
            make_snapshot(processes=250)
        )

        self.assertTrue(
            any("processes" in item.lower() for item in report.anomalies)
        )


if __name__ == "__main__":
    unittest.main()