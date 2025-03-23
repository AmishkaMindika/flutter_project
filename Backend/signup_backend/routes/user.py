from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserResponse
from database import user_collection
from passlib.context import CryptContext
from bson import ObjectId

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = pwd_context.hash(user.password)
    user_data = {"username": user.username, "email": user.email, "password": hashed_password}
    
    new_user = await user_collection.insert_one(user_data)
    
    return UserResponse(
        id=str(new_user.inserted_id),
        username=user.username,
        email=user.email
    )
