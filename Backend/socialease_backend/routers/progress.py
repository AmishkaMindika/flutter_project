from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Progress
from schemas import ProgressSchema
from statistics import mean

router = APIRouter()

@router.get("/progress/{user_id}")
def get_weekly_progress(user_id: int, db: Session = Depends(get_db)):
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    # Fetch progress for the last 7 days
    progress_records = db.query(Progress).filter(
        Progress.user_id == user_id, 
        Progress.day >= seven_days_ago.strftime("%A")  # Filtering by day name
    ).all()

    if not progress_records:
        raise HTTPException(status_code=404, detail="No progress data found")

    # Convert to JSON response
    progress_data = [{"day": p.day, "score": p.score} for p in progress_records]

    # Calculate average score
    avg_score = mean([p["score"] for p in progress_data])

    return {
        "weekly_progress": progress_data,
        "average_score": round(avg_score, 1)
    }
