from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# create post schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# extend PostBase schema
class PostCreate(PostBase):
    pass

# define schema for user response
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

# define schema to return Post Response to a user
class Post(PostBase):
    id: int
    created_at:datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

# define schema for Post Output
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# define schema for users
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# define schema for user response
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# define schema for Token
class Token(BaseModel):
    access_token: str
    token_type: str

# define schema for Token Data
class TokenData(BaseModel):
    id: Optional[str] = None

# define schema for Vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)