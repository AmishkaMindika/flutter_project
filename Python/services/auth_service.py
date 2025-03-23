from models.user import User
from utils.security import hash_password, check_password, generate_token
from utils.validators import validate_email, validate_password

class AuthService:
    def __init__(self, db):
        self.users_collection = db['users']
    
    def register_user(self, email, password, profile=None):
        # Validate email
        if not validate_email(email):
            return None, "Invalid email format"
        
        # Validate password
        is_valid, password_error = validate_password(password)
        if not is_valid:
            return None, password_error
        
        # Check if user exists
        if self.users_collection.find_one({'email': email}):
            return None, "Email already registered"
        
        # Create new user
        hashed_password = hash_password(password)
        user = User(email, hashed_password, profile)
        
        # Save to database
        self.users_collection.insert_one(user.to_dict(include_password=True))
        
        # Generate token
        token = generate_token(email)
        
        return token, None
    
    def login_user(self, email, password):
        # Find user
        user_data = self.users_collection.find_one({'email': email})
        if not user_data:
            return None, "Invalid email or password"
        
        # Check password
        if not check_password(password, user_data['password_hash']):
            return None, "Invalid email or password"
        
        # Generate token
        token = generate_token(email)
        
        return token, None