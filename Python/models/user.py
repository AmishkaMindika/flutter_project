from datetime import datetime

class User:
    def __init__(self, email, password_hash, profile=None):
        self.email = email
        self.password_hash = password_hash
        self.profile = profile or {}
        self.created_at = datetime.utcnow()
    
    def to_dict(self, include_password=False):
        user_dict = {
            'email': self.email,
            'profile': self.profile,
            'created_at': self.created_at
        }
        
        if include_password:
            user_dict['password_hash'] = self.password_hash
            
        return user_dict