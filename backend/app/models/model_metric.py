"""
Model metric model for ML performance tracking
"""

from sqlalchemy import Column, String, Numeric, Integer, Date, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

from backend.app.models.base import Base, UUIDMixin


class ModelMetric(Base, UUIDMixin):
    """Model metric for tracking ML model performance"""
    
    __tablename__ = "model_metrics"
    
    # Model information
    model_version = Column(String(50), nullable=False, index=True)
    
    # Metric information
    metric_type = Column(String(50), nullable=False, index=True)  # accuracy, precision, recall, f1_score
    metric_value = Column(Numeric(5, 4), nullable=False)
    disease_class = Column(String(100))  # Specific disease class or null for overall
    
    # Evaluation information
    evaluation_date = Column(Date, nullable=False, index=True)
    sample_size = Column(Integer)
    notes = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<ModelMetric(id={self.id}, model_version={self.model_version}, metric_type={self.metric_type}, value={self.metric_value})>"
