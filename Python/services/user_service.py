class UserService:
    def __init__(self, db):
        self.users_collection = db['users']
    
    def get_user_profile(self, email):
        user = self.users_collection.find_one({'email': email}, {'password_hash': 0})
        if not user:
            return None
        
        # Convert ObjectId to string for JSON serialization
        if '_id' in user:
            user['_id'] = str(user['_id'])
            
        return user
    
    def update_user_profile(self, email, profile_data):
        result = self.users_collection.update_one(
            {'email': email},
            {'$set': {'profile': profile_data}}
        )
        
        if result.modified_count == 0:
            return False, "User not found or no changes made"
            
        return True, None