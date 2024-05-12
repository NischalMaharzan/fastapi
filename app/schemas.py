from typing import List, Union, Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import BaseModel, Field, validator

from enum import IntEnum
# from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    author: str 
    is_published: Optional[bool]=True
    # rating: Optional[int]= None 


class PostCreate(PostBase):
    pass

class UserBase(BaseModel):
    user_id : int
    email : str


class User(UserBase):
    created_at : datetime
    class Config:
        orm_mode: True

# this is for response.model where the post is actaully retrieved from dabatabse using sqlalchemy Module and neede to be converted to pydantic model i.e dict
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode: True


class Postwithvote(BaseModel):
    Post : Post
    votes: int

    class Config:
        orm_mode: True

class UpdatePost(BaseModel):
    title: str
    author: str
    is_published: Optional[bool]=True





class GetUser(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None











class Vote(BaseModel):
    data: str
    
    class Config:
        orm_mode: True


class TakeVote(BaseModel):
    post_id: int
    dir: int

    @validator('dir')
    def validate_dir(cls, v):
        if v not in (0, 1):
            raise ValueError('dir must be either 0 or 1')
        return v
