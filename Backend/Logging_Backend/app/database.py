from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGO_URI)
db = client.mysdgp  # Select database
users_collection = db.users  # Select users collection
