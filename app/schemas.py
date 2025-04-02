from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# This Python class represents a post with attributes for title, content, and published status.
# class Post(BaseModel):
#     title : str
#     content : str
#     published : bool


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    pass


class UserCreateResponse(BaseModel):
    id_number: int
    name: str
    email: EmailStr
    created_at: datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

class GetPostResponse(PostBase):
    id_number: int
    created_at: datetime
    owner_email: EmailStr
    owner: UserCreateResponse


class UserCreate(UserBase):
    pass


class GetUserResponse(UserCreateResponse):
    pass

class PostResponse(BaseModel):
    Post : GetPostResponse
    votes: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: int