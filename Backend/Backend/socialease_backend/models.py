from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# Progress Tracking Model
class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    day = Column(String(10), nullable=False)  # e.g., "Monday"
    score = Column(Float, nullable=False)

# Notification Settings Model
class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
