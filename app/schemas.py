from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class PostSchema(BaseModel):
    title: str
    content: str

class CommentSchema(BaseModel):
    post_id: int
    content: str
