"""
Weather alert model for extreme weather notifications
"""

from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.app.models.base import Base, UUIDMixin


class AlertType(str, enum.Enum):
    """Weather alert type enumeration"""
    HEAVY_RAIN = "heavy_rain"
    FROST = "frost"
    HEAT_WAVE = "heat_wave"
    HAIL = "hail"
    STORM = "storm"
    DROUGHT = "drought"
    FLOOD = "flood"


class AlertSeverity(str, enum.Enum):
    """Alert severity enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WeatherAlert(Base, UUIDMixin):
    """Weather alert model for extreme weather notifications"""
    
    __tablename__ = "weather_alerts"
    
    # Foreign keys
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Alert information
    alert_type = Column(SQLEnum(AlertType), nullable=False, index=True)
    severity = Column(SQLEnum(AlertSeverity), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Recommendations
    recommended_actions = Column(JSONB)  # Array of action items
    
    # Timing
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime)
    
    # Status
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    is_notified = Column(Boolean, default=False, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    field = relationship("Field", back_populates="weather_alerts")
    user = relationship("User", back_populates="weather_alerts")
    
    def __repr__(self):
        return f"<WeatherAlert(id={self.id}, alert_type={self.alert_type}, severity={self.severity})>"
