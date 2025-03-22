from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: test 01
    email: EmailStr
    password: str
