
from typing import Optional
from pydantic import BaseModel, Field

from .base import BaseNetworkModel
from .user import UserOut


class BasePost(BaseModel):
    """ Base post schema. """
    title: str = Field(..., example='My Post', max_length=50)
    content: str = Field(..., example='This is my post content.')
    topic: Optional[str] = Field(None, example='My Subject', max_length=50)


class PostCreate(BasePost):
    """ Post create schema. """
    pass


class PostUpdate(BasePost):
    """ Post update schema. """
    id: int = Field(..., example=1)


class PostOut(BasePost, BaseNetworkModel):
    """ Post visible data schema. """
    author: UserOut = Field(..., description="Post author")
    likes: int = Field(..., example=0)

    class Config:
        orm_mode = True
