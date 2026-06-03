from typing import Dict
from datetime import datetime, timezone
import time, structlog

logger = structlog.get_logger()

class MetricsCollector:
    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, float] = {}
        self._start_time = time.time()

    def increment(self, name: str, value: int = 1):
        self._counters[name] = self._counters.get(name, 0) + value

    def set_gauge(self, name: str, value: float):
        self._gauges[name] = value

    def get_uptime(self) -> float:
        return time.time() - self._start_time

    def export_prometheus(self) -> str:
        lines = []
        for name, value in self._counters.items():
            lines.append(f"civic_pulse_{name} {value}")
        for name, value in self._gauges.items():
            lines.append(f"civic_pulse_{name} {value}")
        lines.append(f"civic_pulse_uptime_seconds {self.get_uptime()}")
        return "\n".join(lines)

    def get_summary(self) -> Dict:
        return {"counters": self._counters, "gauges": self._gauges, "uptime_seconds": self.get_uptime()}

metrics = MetricsCollector()
