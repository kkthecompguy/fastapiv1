from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional, List

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    owner: UserOut


    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    data: PostOut


class ListPostResponse(BaseModel):
    data: List[PostOut]


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserResponse(BaseModel):
    success: bool
    code: int
    data: UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str     


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)