from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = "mongodb://localhost:27017"  # Change if using cloud MongoDB
DB_NAME = "user_db"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
user_collection = database.get_collection("users")
