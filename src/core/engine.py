from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
from uuid import UUID
import structlog
from src.models.request import RequestStatus, Priority
from src.core.cache import get_cache, set_cache

logger = structlog.get_logger()

SLA_HOURS = {Priority.LOW: 120, Priority.NORMAL: 72, Priority.HIGH: 24, Priority.URGENT: 8, Priority.CRITICAL: 2}

class ProcessingEngine:
    def __init__(self):
        self._processors: Dict[str, callable] = {}
        self._validators: Dict[str, callable] = {}

    def register_processor(self, service_slug: str, processor: callable):
        self._processors[service_slug] = processor

    def register_validator(self, service_slug: str, validator: callable):
        self._validators[service_slug] = validator

    async def classify_request(self, subject: str, description: str, form_data: dict) -> Priority:
        urgent_keywords = ["emergency", "urgent", "critical", "darurat", "segera"]
        text = f"{subject} {description}".lower()
        if any(kw in text for kw in urgent_keywords):
            return Priority.URGENT
        return Priority.NORMAL

    def calculate_deadline(self, priority: Priority, submitted_at: datetime) -> datetime:
        hours = SLA_HOURS.get(priority, 72)
        return submitted_at + timedelta(hours=hours)

    async def process_request(self, request_id: UUID, service_slug: str, data: dict) -> Dict[str, Any]:
        processor = self._processors.get(service_slug)
        if processor is None:
            return {"status": "queued", "message": "Request queued for manual processing"}
        try:
            return await processor(data)
        except Exception as e:
            return {"status": "error", "message": str(e)}

engine = ProcessingEngine()
