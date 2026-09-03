"""System monitoring models and implementations with resilient error handling."""

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from random import randint, uniform

import psutil

logger = logging.getLogger(__name__)


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
    """Collect real-time information from the operating system with safe fallbacks."""

    def collect_snapshot(self) -> SystemSnapshot:
        """Collect current system state defensively to avoid crashes on permission/hardware faults."""
        now = datetime.now()

        # Resilient CPU read
        try:
            cpu_percent = float(psutil.cpu_percent(interval=1))
        except (psutil.Error, OSError) as exc:
            logger.warning("Failed to collect CPU metrics: %s", exc)
            cpu_percent = 0.0

        # Resilient Memory read
        try:
            memory_percent = float(psutil.virtual_memory().percent)
        except (psutil.Error, OSError) as exc:
            logger.warning("Failed to collect Memory metrics: %s", exc)
            memory_percent = 0.0

        # Resilient Disk read
        try:
            disk_percent = float(psutil.disk_usage(os.path.abspath(os.sep)).percent)
        except (psutil.Error, OSError) as exc:
            logger.warning("Failed to collect Disk metrics: %s", exc)
            disk_percent = 0.0

        # Resilient Network read
        try:
            network = psutil.net_io_counters()
            sent_bytes = network.bytes_sent if network else 0
            recv_bytes = network.bytes_recv if network else 0
        except (psutil.Error, OSError) as exc:
            logger.warning("Failed to collect Network metrics: %s", exc)
            sent_bytes = 0
            recv_bytes = 0

        # Resilient Process count
        try:
            running_processes = len(psutil.pids())
        except (psutil.Error, OSError) as exc:
            logger.warning("Failed to collect Process metrics: %s", exc)
            running_processes = 0

        return SystemSnapshot(
            timestamp=now,
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_percent=disk_percent,
            network_sent_bytes=sent_bytes,
            network_received_bytes=recv_bytes,
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