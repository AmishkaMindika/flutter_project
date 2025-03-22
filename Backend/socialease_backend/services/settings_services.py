from sqlalchemy.orm import Session
from models import NotificationSettings
from schemas import NotificationSettingsSchema

def get_settings(db: Session, user_id: int):
    return db.query(NotificationSettings).filter(NotificationSettings.user_id == user_id).first()

def update_settings(db: Session, user_id: int, settings: NotificationSettingsSchema):
    db_settings = db.query(NotificationSettings).filter(NotificationSettings.user_id == user_id).first()
    if db_settings:
        db_settings.email_notifications = settings.email_notifications
        db_settings.push_notifications = settings.push_notifications
        db.commit()
        return db_settings
    return None
