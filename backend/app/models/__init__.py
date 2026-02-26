"""
SQLAlchemy models for the Agriculture Platform
"""

from backend.app.models.base import Base
from backend.app.models.user import User
from backend.app.models.field import Field
from backend.app.models.crop_record import CropRecord
from backend.app.models.image_inference import ImageInference
from backend.app.models.recommendation import Recommendation
from backend.app.models.chat_history import ChatHistory
from backend.app.models.weather_alert import WeatherAlert
from backend.app.models.irrigation_schedule import IrrigationSchedule
from backend.app.models.device_token import DeviceToken
from backend.app.models.system_log import SystemLog
from backend.app.models.model_metric import ModelMetric

__all__ = [
    "Base",
    "User",
    "Field",
    "CropRecord",
    "ImageInference",
    "Recommendation",
    "ChatHistory",
    "WeatherAlert",
    "IrrigationSchedule",
    "DeviceToken",
    "SystemLog",
    "ModelMetric",
]
