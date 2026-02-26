"""
Chat history model for chatbot conversations
"""

from sqlalchemy import Column, String, Text, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.models.base import Base, UUIDMixin


class ChatHistory(Base, UUIDMixin):
    """Chat history model for storing chatbot conversations"""
    
    __tablename__ = "chat_history"
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Conversation data
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    language = Column(String(10), default="en", nullable=False, index=True)
    
    # Metadata
    confidence = Column(Numeric(5, 2))
    sources = Column(JSONB)  # Array of knowledge base sources
    
    # Feedback
    feedback_rating = Column(Integer)  # 1-5 star rating
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_history")
    field = relationship("Field", back_populates="chat_history")
    
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, language={self.language})>"
