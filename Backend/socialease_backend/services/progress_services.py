from sqlalchemy.orm import Session
from models import Progress
from schemas import ProgressSchema

def add_progress(db: Session, progress: ProgressSchema):
    new_progress = Progress(user_id=progress.user_id, day=progress.day, score=progress.score)
    db.add(new_progress)
    db.commit()
    return new_progress

def get_progress(db: Session, user_id: int):
    return db.query(Progress).filter(Progress.user_id == user_id).all()
