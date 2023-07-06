
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., description="User email, must be unique", example="example@gmail.com", max_length=254)
    username: str = Field(..., description="User username, must be unique", example="example1234", max_length=50)
    first_name: str = Field(..., description="User first name", example="John", max_length=50)
    last_name: Optional[str] = Field(None, description="User last name", example="Deer", max_length=50)


class UserSignUp(UserBase):
    """ User sign up schema. """
    password: str = Field(..., description="User password", example="password1234", exclude=True)


class UserOut(UserBase):
    """ User visible data schema. """
    pass

    class Config:
        orm_mode = True
