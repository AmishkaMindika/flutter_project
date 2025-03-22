import re

def validate_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(email_pattern.match(email))

def validate_password(password):
    # Minimum 8 characters, at least one letter and one number
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    
    return True, ""