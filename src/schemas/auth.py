
from pydantic import BaseModel, Field


class Token(BaseModel):
    """ Token schema to return to the user. """
    access_token: str = Field(..., example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLC')
    token_type: str = Field('bearer', example='bearer')
