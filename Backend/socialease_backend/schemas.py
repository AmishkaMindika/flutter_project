from pydantic import BaseModel, Field
from typing import Optional

# Notification Settings Schema
class NotificationSettingsSchema(BaseModel):
    user_id: int
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True

    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes

# Progress Schema
class ProgressSchema(BaseModel):
    user_id: str = Field(..., description="User ID must be a string")  # Changed to string
    day: int = Field(..., description="Day must be a valid integer starting from 1")  # Changed to int
    score: int = Field(..., description="Score must be an integer")

    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes
