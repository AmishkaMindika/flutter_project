from pymongo import MongoClient

# MongoDB Database URL
DATABASE_URL = "mongodb://socialease:sgkl01031308@localhost:27017"

# Create MongoDB Client
client = MongoClient("mongodb+srv://socialease:sgkl01031308@cluster0.yo2mm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Access the database
db = client["socialease"]
collection = db["progress"]

document = {
    "user_id": "kabiz",
    "day": 7,
    "score": 100
}






insert_doc = collection.insert_one(document)

print("inserted doc id = " + str(insert_doc.inserted_id))

# Dependency to get a database connection
def get_db():
    try:
        yield db  # Ensure this is yielding the correct MongoDB database instance
    finally:
        pass
