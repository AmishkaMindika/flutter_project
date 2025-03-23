import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from socialease_backend.models import notifications_collection

# Get notification settings for a user
def get_notification_settings(user_id: int):
    return notifications_collection.find_one({"user_id": user_id})

# Update notification settings for a user
def update_notification_settings(user_id: int, email_notifications: bool, push_notifications: bool):
    settings = {
        "user_id": user_id,
        "email_notifications": email_notifications,
        "push_notifications": push_notifications,
    }
    notifications_collection.update_one(
        {"user_id": user_id}, {"$set": settings}, upsert=True
    )
    return settings

# Send notification if notifications are turned on
def send_notification(user_id: int, message: str):
    settings = notifications_collection.find_one({"user_id": user_id})
    if not settings:
        return {"message": "Notification settings not found for the user."}

    if settings.get("email_notifications") or settings.get("push_notifications"):
        # Simulate sending a notification
        print(f"Notification sent to user {user_id}: {message}")
        return {"message": f"Notification sent to user {user_id}"}
    else:
        return {"message": f"Notifications are turned off for user {user_id}."}
