"""Terminal dashboard for the Digital Twin."""

from digital_twin.health import HealthReport
from digital_twin.monitoring import SystemSnapshot


class Dashboard:
    """Displays the current Digital Twin state in the terminal."""

    def render(
        self,
        snapshot: SystemSnapshot | None = None,
        report: HealthReport | None = None,
    ) -> None:
        print()
        print("=" * 60)
        print("              DIGITAL TWIN DASHBOARD")
        print("=" * 60)

        if snapshot is None:
            print("No system data available.")
            return

        print(f"Timestamp:          {snapshot.timestamp}")
        print()
        print(f"CPU Usage:          {snapshot.cpu_percent}%")
        print(f"Memory Usage:       {snapshot.memory_percent}%")
        print(f"Disk Usage:         {snapshot.disk_percent}%")
        print(f"Running Processes:  {snapshot.running_processes}")
        print(f"Network Sent:       {snapshot.network_sent_bytes:,} bytes")
        print(f"Network Received:   {snapshot.network_received_bytes:,} bytes")

        print("-" * 60)

        if report is not None:
            print(f"Health Score:       {report.score}/100")
            print(f"System Status:      {report.status.value.upper()}")

            if report.messages:
                print("\nAlerts:")
                for message in report.messages:
                    print(f"  ⚠ {message}")
            else:
                print("\nAlerts:             None")

            if report.anomalies:
                print("\nAnomalies:")
                for anomaly in report.anomalies:
                    print(f"  ! {anomaly}")

            if report.recommendations:
                print("\nRecommendations:")
                for recommendation in report.recommendations:
                    print(f"  → {recommendation}")

        print("=" * 60)