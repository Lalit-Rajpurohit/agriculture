"""
Image inference model for disease detection results
"""

from sqlalchemy import Column, String, Numeric, Integer, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.app.models.base import Base, UUIDMixin


class InferenceType(str, enum.Enum):
    """Inference type enumeration"""
    ON_DEVICE = "on_device"
    SERVER = "server"


class ImageInference(Base, UUIDMixin):
    """Image inference model for storing disease detection results"""
    
    __tablename__ = "image_inferences"
    
    # Foreign keys
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Image information
    image_url = Column(String(500), nullable=False)
    image_s3_key = Column(String(500), nullable=False)
    
    # Prediction results
    predictions = Column(JSONB, nullable=False)  # Array of {disease, confidence, severity}
    top_disease = Column(String(100), index=True)
    top_confidence = Column(Numeric(5, 2), index=True)
    
    # Inference metadata
    inference_type = Column(SQLEnum(InferenceType), nullable=False, index=True)
    inference_duration_ms = Column(Integer)
    model_version = Column(String(50))
    
    # Feedback
    is_feedback_provided = Column(Boolean, default=False, nullable=False)
    feedback_correct = Column(Boolean)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    field = relationship("Field", back_populates="image_inferences")
    user = relationship("User", back_populates="image_inferences")
    recommendations = relationship("Recommendation", back_populates="inference", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ImageInference(id={self.id}, top_disease={self.top_disease}, confidence={self.top_confidence})>"
