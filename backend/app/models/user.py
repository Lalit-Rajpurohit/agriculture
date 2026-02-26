"""
User model for farmers and administrators
"""

from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from backend.app.models.base import Base, UUIDMixin, TimestampMixin


class UserRole(str, enum.Enum):
    """User role enumeration"""
    FARMER = "farmer"
    ADMIN = "admin"


class User(Base, UUIDMixin, TimestampMixin):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.FARMER, nullable=False, index=True)
    
    # Profile fields
    full_name = Column(String(255))
    phone_number = Column(String(20))
    language_preference = Column(String(10), default="en")
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    fields = relationship("Field", back_populates="user", cascade="all, delete-orphan")
    image_inferences = relationship("ImageInference", back_populates="user", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    weather_alerts = relationship("WeatherAlert", back_populates="user", cascade="all, delete-orphan")
    irrigation_schedules = relationship("IrrigationSchedule", back_populates="user", cascade="all, delete-orphan")
    device_tokens = relationship("DeviceToken", back_populates="user", cascade="all, delete-orphan")
    system_logs = relationship("SystemLog", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
