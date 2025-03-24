from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, crud, schemas
from app.routes.auth import get_db

router = APIRouter(prefix="/community", tags=["Community"])

@router.post("/post")
def create_post(post: schemas.PostSchema, user_id: int, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post, user_id=user_id)

@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db=db)

@router.post("/comment")
def create_comment(comment: schemas.CommentSchema, user_id: int, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, user_id=user_id)
