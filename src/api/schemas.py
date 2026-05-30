from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class CitizenCreate(BaseModel):
    citizen_id: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    phone: Optional[str] = None
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8)
    address: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None

class CitizenResponse(BaseModel):
    id: UUID
    citizen_id: str
    email: str
    full_name: str
    is_verified: bool
    created_at: datetime
    class Config:
        from_attributes = True

class CitizenLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class ServiceResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str
    processing_time_hours: int
    fee_amount: float
    is_online: bool
    department: Optional[str]
    class Config:
        from_attributes = True

class ServiceRequestCreate(BaseModel):
    service_id: UUID
    subject: str = Field(..., min_length=5, max_length=500)
    description: Optional[str] = None
    form_data: Dict[str, Any] = {}

class ServiceRequestResponse(BaseModel):
    id: UUID
    request_number: str
    status: str
    priority: str
    subject: str
    created_at: datetime
    class Config:
        from_attributes = True

class ServiceStats(BaseModel):
    total_requests: int
    pending_requests: int
    completed_requests: int
    avg_processing_hours: float
    satisfaction_rate: float
