from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from uuid import UUID
import structlog
from src.models.request import RequestStatus, Priority
from src.services.notification import notification_service, NotificationType

logger = structlog.get_logger()

VALID_TRANSITIONS = {
    RequestStatus.DRAFT: [RequestStatus.SUBMITTED, RequestStatus.CANCELLED],
    RequestStatus.SUBMITTED: [RequestStatus.UNDER_REVIEW, RequestStatus.CANCELLED],
    RequestStatus.UNDER_REVIEW: [RequestStatus.IN_PROGRESS, RequestStatus.ADDITIONAL_INFO_REQUIRED, RequestStatus.REJECTED],
    RequestStatus.ADDITIONAL_INFO_REQUIRED: [RequestStatus.UNDER_REVIEW, RequestStatus.CANCELLED],
    RequestStatus.IN_PROGRESS: [RequestStatus.PENDING_APPROVAL, RequestStatus.REJECTED],
    RequestStatus.PENDING_APPROVAL: [RequestStatus.APPROVED, RequestStatus.REJECTED, RequestStatus.IN_PROGRESS],
    RequestStatus.APPROVED: [RequestStatus.COMPLETED],
    RequestStatus.REJECTED: [],
    RequestStatus.COMPLETED: [],
    RequestStatus.CANCELLED: [],
}

class WorkflowService:
    def validate_transition(self, current: RequestStatus, target: RequestStatus) -> bool:
        return target in VALID_TRANSITIONS.get(current, [])

    async def transition_request(self, db, request, target_status: RequestStatus, actor: str, notes: Optional[str] = None) -> bool:
        if not self.validate_transition(request.status, target_status):
            return False
        old_status = request.status
        request.status = target_status
        request.updated_at = datetime.now(timezone.utc)
        if request.notes is None: request.notes = []
        request.notes.append({"timestamp": datetime.now(timezone.utc).isoformat(), "actor": actor,
                              "from": old_status.value, "to": target_status.value, "notes": notes})
        if target_status == RequestStatus.SUBMITTED: request.submitted_at = datetime.now(timezone.utc)
        elif target_status in (RequestStatus.COMPLETED, RequestStatus.REJECTED): request.completed_at = datetime.now(timezone.utc)
        logger.info("request_transitioned", request_id=str(request.id), from_status=old_status.value, to=target_status.value)
        return True

workflow_service = WorkflowService()
