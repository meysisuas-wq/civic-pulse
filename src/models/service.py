from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from src.db.database import Base

class ServiceCategory(Base):
    __tablename__ = "service_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(7), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    services = relationship("Service", back_populates="category", lazy="selectin")

class Service(Base):
    __tablename__ = "services"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)
    requirements = Column(JSONB, default=list)
    processing_time_hours = Column(Integer, default=72)
    fee_amount = Column(Float, default=0.0)
    fee_currency = Column(String(3), default="IDR")
    is_online = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    department = Column(String(200), nullable=True)
    tags = Column(ARRAY(String), default=list)
    avg_rating = Column(Float, default=0.0)
    total_requests = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    category = relationship("ServiceCategory", back_populates="services")
    requests = relationship("ServiceRequest", back_populates="service", lazy="selectin")
