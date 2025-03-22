from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import NotificationSettings
from schemas import NotificationSettingsSchema

router = APIRouter()

@router.get("/settings/{user_id}", response_model=NotificationSettingsSchema)
def get_settings(user_id: int, db: Session = Depends(get_db)):
    settings = db.query(NotificationSettings).filter(NotificationSettings.user_id == user_id).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/settings/{user_id}")
def update_settings(user_id: int, settings: NotificationSettingsSchema, db: Session = Depends(get_db)):
    db_settings = db.query(NotificationSettings).filter(NotificationSettings.user_id == user_id).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    
    db_settings.email_notifications = settings.email_notifications
    db_settings.push_notifications = settings.push_notifications
    db.commit()
    return {"message": "Settings updated"}
