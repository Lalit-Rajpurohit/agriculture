"""
Device token model for push notifications
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.app.models.base import Base, UUIDMixin


class DeviceType(str, enum.Enum):
    """Device type enumeration"""
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class DeviceToken(Base, UUIDMixin):
    """Device token model for push notification management"""
    
    __tablename__ = "device_tokens"
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Token information
    token = Column(String(500), unique=True, nullable=False, index=True)
    device_type = Column(SQLEnum(DeviceType), nullable=False)
    device_info = Column(JSONB)  # Device model, OS version, app version
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    last_used_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="device_tokens")
    
    def __repr__(self):
        return f"<DeviceToken(id={self.id}, device_type={self.device_type}, is_active={self.is_active})>"
