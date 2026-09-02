"""System monitoring models and implementations."""

import os
from dataclasses import dataclass
from datetime import datetime
from random import randint, uniform

import psutil


@dataclass(frozen=True)
class SystemSnapshot:
    """A point-in-time view of the computer system."""

    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_sent_bytes: int
    network_received_bytes: int
    running_processes: int


class SystemMonitor:
    """Collect real-time information from the operating system."""

    def collect_snapshot(self) -> SystemSnapshot:
        """Collect the current system state using psutil."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage(os.path.abspath(os.sep)).percent
        network = psutil.net_io_counters()
        running_processes = len(psutil.pids())

        return SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_percent=disk_percent,
            network_sent_bytes=network.bytes_sent,
            network_received_bytes=network.bytes_recv,
            running_processes=running_processes,
        )


class SimulatedSystemMonitor:
    """Generates realistic simulated system measurements."""

    def collect_snapshot(self) -> SystemSnapshot:
        return SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=round(uniform(20, 85), 1),
            memory_percent=round(uniform(30, 80), 1),
            disk_percent=round(uniform(20, 70), 1),
            network_sent_bytes=randint(1_000_000, 20_000_000),
            network_received_bytes=randint(2_000_000, 50_000_000),
            running_processes=randint(80, 180),
        )
