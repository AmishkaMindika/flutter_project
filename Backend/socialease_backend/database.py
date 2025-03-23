from pymongo import MongoClient

# MongoDB Database URL
DATABASE_URL = "mongodb://username:password@localhost:27017"

# Create MongoDB Client
client = MongoClient(DATABASE_URL)

# Access the database
db = client["socialease"]

# Dependency to get a database connection
def get_db():
    try:
        yield db
    finally:
        pass  # Removed client.close() to avoid errors
