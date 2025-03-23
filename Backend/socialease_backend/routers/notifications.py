from fastapi import APIRouter, HTTPException
from socialease_backend.services.notification_services import (
    get_notification_settings,
    update_notification_settings,

    send_notification,  # Import the new function
)

router = APIRouter()

@router.get("/notifications/{user_id}")
def read_notification_settings(user_id: int):
    settings = get_notification_settings(user_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    return settings

@router.post("/notifications/{user_id}")
def set_notification_settings(user_id: int, email_notifications: bool, push_notifications: bool):
    updated_settings = update_notification_settings(user_id, email_notifications, push_notifications)
    return {"message": "Notification settings updated", "settings": updated_settings}

@router.post("/notifications/{user_id}/send")
def trigger_notification(user_id: int, message: str):
    result = send_notification(user_id, message)
    return result
