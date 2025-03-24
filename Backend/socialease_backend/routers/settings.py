from fastapi import APIRouter, Depends
from socialease_backend.database import get_db
from socialease_backend.services.settings_services import get_settings, update_settings
from socialease_backend.schemas import NotificationSettingsSchema

router = APIRouter()

@router.get("/settings/{user_id}")
def read_settings(user_id: int, db=Depends(get_db)):
    return get_settings(db, user_id)

@router.put("/settings/{user_id}")
def modify_settings(user_id: int, settings: NotificationSettingsSchema, db=Depends(get_db)):
    return update_settings(db, user_id, settings)
