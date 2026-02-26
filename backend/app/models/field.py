"""
Field model for agricultural land management
"""

from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDMixin, TimestampMixin


class Field(Base, UUIDMixin, TimestampMixin):
    """Field model representing agricultural land parcels"""
    
    __tablename__ = "fields"
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Field information
    name = Column(String(255), nullable=False)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    area_hectares = Column(Numeric(10, 2), nullable=False)
    
    # Soil and crop information
    soil_type = Column(String(50))  # clay, loam, sandy, silt, etc.
    crop_type = Column(String(100), nullable=False, index=True)
    sowing_date = Column(Date, nullable=False, index=True)
    expected_harvest_date = Column(Date)
    irrigation_type = Column(String(50))  # drip, sprinkler, flood, rainfed
    
    # Relationships
    user = relationship("User", back_populates="fields")
    crop_records = relationship("CropRecord", back_populates="field", cascade="all, delete-orphan")
    image_inferences = relationship("ImageInference", back_populates="field", cascade="all, delete-orphan")
    weather_alerts = relationship("WeatherAlert", back_populates="field", cascade="all, delete-orphan")
    irrigation_schedules = relationship("IrrigationSchedule", back_populates="field", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="field")
    
    def __repr__(self):
        return f"<Field(id={self.id}, name={self.name}, crop_type={self.crop_type})>"
