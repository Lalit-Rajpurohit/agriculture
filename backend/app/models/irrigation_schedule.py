"""
Irrigation schedule model for water management
"""

from sqlalchemy import Column, Numeric, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.models.base import Base, UUIDMixin


class IrrigationSchedule(Base, UUIDMixin):
    """Irrigation schedule model for water management recommendations"""
    
    __tablename__ = "irrigation_schedules"
    
    # Foreign keys
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Schedule information
    recommended_date = Column(DateTime, nullable=False, index=True)
    water_volume_liters = Column(Numeric(10, 2), nullable=False)
    
    # Input parameters
    soil_moisture_level = Column(Numeric(5, 2))  # Percentage
    weather_forecast = Column(JSONB)  # Weather data used for calculation
    reasoning = Column(Text)
    
    # Completion tracking
    is_completed = Column(Boolean, default=False, nullable=False, index=True)
    completed_at = Column(DateTime)
    actual_water_used_liters = Column(Numeric(10, 2))
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    field = relationship("Field", back_populates="irrigation_schedules")
    user = relationship("User", back_populates="irrigation_schedules")
    
    def __repr__(self):
        return f"<IrrigationSchedule(id={self.id}, recommended_date={self.recommended_date}, water_volume={self.water_volume_liters})>"
