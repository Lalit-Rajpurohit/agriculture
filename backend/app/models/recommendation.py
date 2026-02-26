"""
Recommendation model for treatment advice
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.models.base import Base, UUIDMixin


class Recommendation(Base, UUIDMixin):
    """Recommendation model for disease treatment advice"""
    
    __tablename__ = "recommendations"
    
    # Foreign keys
    inference_id = Column(UUID(as_uuid=True), ForeignKey("image_inferences.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Treatment information
    treatment_type = Column(String(50), nullable=False, index=True)  # chemical, organic, cultural, biological
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Product recommendations
    products = Column(JSONB)  # Array of {name, dosage, application_rate}
    
    # Priority and cost
    priority = Column(Integer, default=1, nullable=False, index=True)  # 1=high, 2=medium, 3=low
    estimated_cost_range = Column(String(50))
    
    # Application details
    application_method = Column(Text)
    precautions = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    inference = relationship("ImageInference", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation(id={self.id}, treatment_type={self.treatment_type}, priority={self.priority})>"
