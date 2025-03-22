import bcrypt
from flask_jwt_extended import create_access_token
import datetime

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def generate_token(identity):
    expires = datetime.timedelta(days=1)
    return create_access_token(identity=identity, expires_delta=expires)