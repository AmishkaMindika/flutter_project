from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["socialease"]

# Define collections
notifications_collection = db["notifications"]


