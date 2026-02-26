"""
Crop record model for historical crop data
"""

from sqlalchemy import Column, String, Date, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.models.base import Base, UUIDMixin


class CropRecord(Base, UUIDMixin):
    """Crop record model for tracking historical crop data"""
    
    __tablename__ = "crop_records"
    
    # Foreign keys
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Crop information
    crop_type = Column(String(100), nullable=False, index=True)
    variety = Column(String(100))
    sowing_date = Column(Date, nullable=False, index=True)
    harvest_date = Column(Date, index=True)
    
    # Yield information
    yield_kg = Column(Numeric(10, 2))
    quality_grade = Column(String(20))
    notes = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    field = relationship("Field", back_populates="crop_records")
    
    def __repr__(self):
        return f"<CropRecord(id={self.id}, crop_type={self.crop_type}, field_id={self.field_id})>"
