"""System health analysis and diagnostic reporting."""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from digital_twin.config import DEFAULT_THRESHOLDS, HealthThresholds
from digital_twin.monitoring import SystemSnapshot


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class HealthReport:
    status: HealthStatus
    score: int
    messages: Tuple[str, ...]
    anomalies: Tuple[str, ...]
    recommendations: Tuple[str, ...]


class SystemHealthAnalyzer:
    """Analyzes system resources and identifies health problems."""

    def __init__(self, thresholds: HealthThresholds = DEFAULT_THRESHOLDS):
        self.thresholds = thresholds

    def analyze(self, snapshot: SystemSnapshot) -> HealthReport:
        score = 100

        messages: list[str] = []
        anomalies: list[str] = []
        recommendations: list[str] = []

        # CPU analysis
        if snapshot.cpu_percent >= self.thresholds.cpu_critical:
            score -= 30
            messages.append("Critical CPU usage.")
            anomalies.append("CPU usage reached a critical level.")
            recommendations.append(
                "Reduce CPU-intensive workloads or close unnecessary applications."
            )
        elif snapshot.cpu_percent >= self.thresholds.cpu_warning:
            score -= 15
            messages.append("High CPU usage.")
            recommendations.append(
                "Monitor CPU usage and reduce heavy workloads if it remains high."
            )

        # Memory analysis
        if snapshot.memory_percent >= self.thresholds.memory_critical:
            score -= 30
            messages.append("Critical memory usage.")
            anomalies.append("Memory usage reached a critical level.")
            recommendations.append(
                "Close unnecessary applications or increase available memory."
            )
        elif snapshot.memory_percent >= self.thresholds.memory_warning:
            score -= 15
            messages.append("High memory usage.")
            recommendations.append(
                "Close unused applications and monitor memory consumption."
            )

        # Disk analysis
        if snapshot.disk_percent >= self.thresholds.disk_critical:
            score -= 20
            messages.append("Critical disk usage.")
            anomalies.append("Disk usage is critically high.")
            recommendations.append(
                "Free disk space by removing unnecessary files or applications."
            )
        elif snapshot.disk_percent >= self.thresholds.disk_warning:
            score -= 10
            messages.append("Disk usage is getting high.")
            recommendations.append(
                "Consider freeing some disk space before storage becomes critical."
            )

        # Process analysis
        if snapshot.running_processes >= self.thresholds.max_recommended_processes:
            score -= 10
            anomalies.append("Unusually high number of running processes.")
            recommendations.append(
                "Review background processes and close unnecessary applications."
            )

        # Final health status
        score = max(score, 0)

        if score >= 80:
            status = HealthStatus.HEALTHY
        elif score >= 60:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        return HealthReport(
            status=status,
            score=score,
            messages=tuple(messages),
            anomalies=tuple(anomalies),
            recommendations=tuple(recommendations),
        )