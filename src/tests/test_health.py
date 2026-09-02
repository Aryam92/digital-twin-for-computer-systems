"""Tests for the Digital Twin health analyzer."""

import unittest
from datetime import datetime

from digital_twin.health import HealthStatus, SystemHealthAnalyzer
from digital_twin.monitoring import SystemSnapshot


class TestSystemHealthAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SystemHealthAnalyzer()

    def test_healthy_system(self):
        snapshot = SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=30,
            memory_percent=40,
            disk_percent=30,
            running_processes=100,
            network_sent_bytes=0,
            network_received_bytes=0,
        )

        report = self.analyzer.analyze(snapshot)

        self.assertEqual(report.status, HealthStatus.HEALTHY)
        self.assertEqual(report.score, 100)
        self.assertEqual(report.anomalies, ())
        self.assertEqual(report.recommendations, ())

    def test_warning_system(self):
        snapshot = SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=75,
            memory_percent=80,
            disk_percent=70,
            running_processes=100,
            network_sent_bytes=0,
            network_received_bytes=0,
        )

        report = self.analyzer.analyze(snapshot)

        self.assertEqual(report.status, HealthStatus.WARNING)
        self.assertTrue(0 < report.score < 80)
        self.assertGreater(len(report.recommendations), 0)

    def test_critical_system(self):
        snapshot = SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=95,
            memory_percent=95,
            disk_percent=95,
            running_processes=250,
            network_sent_bytes=0,
            network_received_bytes=0,
        )

        report = self.analyzer.analyze(snapshot)

        self.assertEqual(report.status, HealthStatus.CRITICAL)
        self.assertTrue(report.score < 60)
        self.assertGreater(len(report.anomalies), 0)
        self.assertGreater(len(report.recommendations), 0)


if __name__ == "__main__":
    unittest.main()