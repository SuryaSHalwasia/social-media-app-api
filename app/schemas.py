from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class postBase(BaseModel):
    title: str
    body: str
    published: bool = True


class postCreate(postBase):
    pass

class userCreate(BaseModel):
    email:EmailStr
    password:str

class userOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class userLogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None
    

class Post(postBase):
    id: int
    created_at: datetime 
    user_id:int
    user:userOut
    class Config:
        orm_mode = True
        from_attributes = True

class PostCreate(postBase):
    id: int
    created_at: datetime 
    user_id:int

    user:userOut
    class Config:
        orm_mode = True
        from_attributes = True


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)

class postOut(BaseModel):
    Post:PostCreate
    votes:int
    
    class Config:
        orm_mode = True
        from_attributes = True
