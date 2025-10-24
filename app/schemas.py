"""
Pydantic schemas for request and response validation.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, UUID4, ConfigDict


class BlacklistCreate(BaseModel):
    """
    Schema for creating a new blacklist entry.
    """
    email: EmailStr = Field(..., description="The email address to blacklist")
    app_uuid: UUID4 = Field(..., description="The client application's unique identifier (UUID)")
    blocked_reason: Optional[str] = Field(None, max_length=255, description="Reason for blacklisting (optional, max 255 chars)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "spammer@example.com",
                "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
                "blocked_reason": "Spam sender"
            }
        }
    )


class BlacklistAddResponse(BaseModel):
    """
    Response schema after successfully adding an email to the blacklist.
    """
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Email 'spammer@example.com' was added to the blacklist successfully"
            }
        }
    )


class BlacklistCheckResponse(BaseModel):
    """
    Response schema for checking if an email is blacklisted.
    """
    is_blacklisted: bool
    reason: Optional[str] = None
    app_uuid: Optional[str] = None
    date_added: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "is_blacklisted": True,
                "reason": "Spam sender",
                "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
                "date_added": "2025-10-13T10:30:00Z"
            }
        }
    )
