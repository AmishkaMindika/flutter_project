import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from socialease_backend.schemas import ProgressSchema  # Updated import

def add_progress(db, progress: ProgressSchema):
    new_progress = {
        "user_id": progress.user_id,
        "day": progress.day,
        "score": progress.score
    }
    db["progress"].insert_one(new_progress)  # Insert into MongoDB collection
    return new_progress  # Removed print statement

def get_progress(db, user_id: int):
    progress_data = list(db["progress"].find({"user_id": user_id}))  # Query MongoDB collection
    return progress_data  # Removed print statements

def display_all_progress(db):
    progress_data = list(db["progress"].find())  # Retrieve all documents from the 'progress' collection
    return progress_data  # Removed print statements

def calculate_weekly_average(db, user_id: int):
    progress_data = list(db["progress"].find({"user_id": user_id}))  # Query MongoDB collection
    if not progress_data:
        print(f"No progress data found for user_id {user_id}")
        return None

    # Group scores by week
    weekly_scores = {}
    for item in progress_data:
        week = (int(item["day"]) - 1) // 7 + 1  # Calculate week number
        if week not in weekly_scores:
            weekly_scores[week] = []
        weekly_scores[week].append(item["score"])

    # Calculate weekly averages
    weekly_averages = {}
    for week, scores in weekly_scores.items():
        weekly_averages[week] = sum(scores) / len(scores)
        print(f"Week {week}: Average Score = {weekly_averages[week]}")

    # Store weekly averages in MongoDB
    for week, avg_score in weekly_averages.items():
        db["weekly_averages"].update_one(
            {"user_id": user_id, "week": week},  # Filter by user_id and week
            {"$set": {"average_score": avg_score}},  # Update or insert average score
            upsert=True  # Insert if not found
        )
        print(f"Stored weekly average for user_id {user_id}, week {week}: {avg_score}")

    return weekly_averages

def calculate_simple_weekly_average(db, user_id: str):
    progress_data = list(db["progress"].find({"user_id": user_id}).sort("day", 1))  # Sort by day in ascending order

    # Take the last 7 days of progress
    last_7_days = progress_data[-7:] if len(progress_data) >= 7 else progress_data

    # Calculate the average score
    if last_7_days:
        total_score = sum(item["score"] for item in last_7_days)
        average_score = total_score / len(last_7_days)

        # Store the average score in MongoDB
        db["weekly_averages"].update_one(
            {"user_id": user_id},  # Filter by user_id
            {"$set": {"average_score": average_score}},  # Update or insert average score
            upsert=True  # Insert if not found
        )
    return average_score if last_7_days else None  # Removed print statements

def calculate_and_save_first_7_scores_average(db, user_id: str):
    # Retrieve progress data for the user, sorted by day
    progress_data = list(db["progress"].find({"user_id": user_id}).sort("day", 1))  # Sort by day in ascending order

    if not progress_data:
        return {"message": f"No progress data found for user_id {user_id}."}

    # Take the first 7 scores
    first_7_scores = progress_data[:7]

    # Calculate the average score
    total_score = sum(item["score"] for item in first_7_scores)
    average_score = total_score / len(first_7_scores)

    # Save the average score in MongoDB
    db["averages"].update_one(
        {"user_id": user_id},  # Filter by user_id
        {"$set": {"average_score": average_score}},  # Update or insert average score
        upsert=True  # Insert if not found
    )

    # Return the scores and average
    return {
        "scores": [item["score"] for item in first_7_scores],
        "average_score": average_score
    }

if __name__ == "__main__":
    from pymongo import MongoClient
    from socialease_backend.schemas import ProgressSchema

    # Create a test MongoDB client
    client = MongoClient("mongodb+srv://socialease:sgkl01031308@cluster0.yo2mm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["socialease"]

    # Corrected test data
    test_progress = ProgressSchema(user_id="kabiz", day=1, score=100)  # Ensure day is an integer starting from 1

    # Call add_progress
    print("Testing add_progress:")
    add_progress(db, test_progress)

    # Call get_progress
    print("\nTesting get_progress:")
    get_progress(db, user_id="kabiz")  # Ensure user_id is passed as a string

    # Display all progress data
    print("\nDisplaying all progress data:")
    display_all_progress(db)

    # Calculate and store weekly averages
    print("\nCalculating and storing weekly averages:")
    calculate_weekly_average(db, user_id=1)

    # Calculate and store simple weekly average
    print("\nCalculating and storing simple weekly average:")
    calculate_simple_weekly_average(db, user_id="kabiz")

    # Calculate, display, and save the average of the first 7 scores
    print("\nCalculating, displaying, and saving the average of the first 7 scores:")
    result = calculate_and_save_first_7_scores_average(db, "kabiz")
    print(result)
