from schemas import NotificationSettingsSchema

def get_settings(db, user_id: int):
    return db["notification_settings"].find_one({"user_id": user_id})  # Query MongoDB collection

def update_settings(db, user_id: int, settings: NotificationSettingsSchema):
    result = db["notification_settings"].update_one(
        {"user_id": user_id},  # Filter by user_id
        {"$set": {
            "email_notifications": settings.email_notifications,
            "push_notifications": settings.push_notifications
        }},
        upsert=True  # Insert if not found
    )
    if result.matched_count > 0 or result.upserted_id:
        return db["notification_settings"].find_one({"user_id": user_id})  # Return updated document
    return None
