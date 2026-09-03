"""Configuration thresholds for the Digital Twin diagnostic engine."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthThresholds:
    # Warning Thresholds (Percentages)
    cpu_warning: float = 70.0
    memory_warning: float = 80.0
    disk_warning: float = 75.0

    # Critical Thresholds (Percentages)
    cpu_critical: float = 90.0
    memory_critical: float = 90.0
    disk_critical: float = 90.0

    # Process Threshold
    max_recommended_processes: int = 200


DEFAULT_THRESHOLDS = HealthThresholds()