"""
SQLAlchemy models for the Blacklist application.
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class BlacklistEntry(Base):
    """
    Model representing an email entry in the global blacklist.
    """
    __tablename__ = "blacklist_entries"

    email = Column(String(255), primary_key=True, index=True, nullable=False)
    app_uuid = Column(String(255), nullable=False)
    blocked_reason = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=False)  # IPv6 can be up to 45 chars
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<BlacklistEntry(email='{self.email}', app_uuid='{self.app_uuid}')>"
