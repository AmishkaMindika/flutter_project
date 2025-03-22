from pydantic import BaseModel
from typing import Optional

# Notification Settings Schema
class NotificationSettingsSchema(BaseModel):
    user_id: int
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True

    class Config:
        orm_mode = True

# Progress Schema
class ProgressSchema(BaseModel):
    user_id: int
    day: str
    score: int

    class Config:
        orm_mode = True
