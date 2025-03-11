from app.database import users_collection
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_by_email(email):
    return users_collection.find_one({"email": email})

def create_user(email, password):
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({"email": email, "password": hashed_password})
