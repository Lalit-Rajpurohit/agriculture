"""
System log model for audit and monitoring
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.models.base import Base, UUIDMixin


class SystemLog(Base, UUIDMixin):
    """System log model for audit trail and monitoring"""
    
    __tablename__ = "system_logs"
    
    # Foreign keys (nullable for system-level logs)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Action information
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), index=True)
    resource_id = Column(UUID(as_uuid=True))
    
    # Request information
    request_method = Column(String(10))
    request_path = Column(String(500))
    status_code = Column(Integer, index=True)
    duration_ms = Column(Integer)
    
    # Client information
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Error information
    error_message = Column(Text)
    
    # Additional metadata
    metadata = Column(JSONB)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="system_logs")
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, action={self.action}, status_code={self.status_code})>"
