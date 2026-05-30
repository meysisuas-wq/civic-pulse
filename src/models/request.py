from sqlalchemy import Column, String, DateTime, Text, Float, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid, enum
from datetime import datetime, timezone
from src.db.database import Base

class RequestStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ADDITIONAL_INFO_REQUIRED = "additional_info_required"
    IN_PROGRESS = "in_progress"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Priority(str, enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_number = Column(String(30), unique=True, nullable=False, index=True)
    citizen_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    service_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.DRAFT, nullable=False, index=True)
    priority = Column(SQLEnum(Priority), default=Priority.NORMAL, nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    form_data = Column(JSONB, default=dict)
    attachments = Column(JSONB, default=list)
    assigned_to = Column(String(255), nullable=True)
    department = Column(String(200), nullable=True)
    notes = Column(JSONB, default=list)
    resolution = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    citizen_rating = Column(Float, nullable=True)
    citizen_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    citizen = relationship("Citizen", back_populates="requests")
    service = relationship("Service", back_populates="requests")
