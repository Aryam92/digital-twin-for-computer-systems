# Digital Twin for Computer Systems

A Python-based digital twin for monitoring, analyzing, and simulating
computer system health.

The project creates a software representation of a real computer by
collecting system metrics, evaluating resource health, detecting anomalies,
and testing hypothetical system conditions through what-if simulations.

## Features

- Real-time CPU monitoring
- Real-time memory monitoring
- Disk space monitoring
- Network traffic monitoring
- Running process monitoring
- Health scoring from 0 to 100
- Healthy / Warning / Critical status classification
- Anomaly detection
- Actionable recommendations
- What-if system simulations
- Terminal dashboard
- Automated unit tests
- Application logging

## Architecture

```text
Real Computer
     |
     v
SystemMonitor
     |
     v
SystemSnapshot
     |
     +----------------------+
     |                      |
     v                      v
Health Analyzer       Simulation Engine
     |                      |
     v                      v
Health Report          Simulated Snapshot
     |                      |
     +----------+-----------+
                |
                v
             Dashboard