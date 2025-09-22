from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

class AgentRegistration(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    email: EmailStr
    geographic_area: str
    main_sector: str
    cv_filename: Optional[str] = None
    cv_file_path: Optional[str] = None
    language: str = "es"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"

class AgentRegistrationCreate(BaseModel):
    full_name: str
    email: EmailStr
    geographic_area: str
    main_sector: str
    language: str = "es"

class AgentRegistrationResponse(BaseModel):
    message: str
    registration_id: str
    email_sent: bool
    cv_saved: bool