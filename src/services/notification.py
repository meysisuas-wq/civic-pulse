from typing import Dict, Any, List
from enum import Enum
import structlog

logger = structlog.get_logger()

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"

class NotificationType(str, Enum):
    REQUEST_SUBMITTED = "request_submitted"
    REQUEST_UPDATED = "request_updated"
    REQUEST_COMPLETED = "request_completed"
    REQUEST_REJECTED = "request_rejected"
    INFO_REQUIRED = "info_required"

TEMPLATES = {
    NotificationType.REQUEST_SUBMITTED: {"title": "Request Submitted", "body": "Your request {request_number} has been submitted."},
    NotificationType.REQUEST_COMPLETED: {"title": "Request Completed", "body": "Your request {request_number} has been completed."},
    NotificationType.INFO_REQUIRED: {"title": "Info Required", "body": "Your request {request_number} requires additional information."},
}

class NotificationService:
    def __init__(self):
        self._channels: Dict[NotificationChannel, callable] = {}

    def register_channel(self, channel: NotificationChannel, sender: callable):
        self._channels[channel] = sender

    async def send(self, recipient: str, notification_type: NotificationType, context: Dict[str, Any],
                   channels: List[NotificationChannel] = None):
        if channels is None:
            channels = [NotificationChannel.EMAIL, NotificationChannel.IN_APP]
        template = TEMPLATES.get(notification_type)
        if not template: return
        title = template["title"]
        body = template["body"].format(**context)
        for channel in channels:
            sender = self._channels.get(channel)
            if sender:
                try:
                    await sender(recipient, title, body, context)
                    logger.info("notification_sent", channel=channel.value, type=notification_type)
                except Exception as e:
                    logger.error("notification_failed", channel=channel.value, error=str(e))

notification_service = NotificationService()
