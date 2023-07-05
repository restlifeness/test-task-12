
from pydantic import BaseModel, Field
from datetime import datetime


class BaseNetworkModel(BaseModel):
    """ Base network schema. """
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example='2021-01-01 00:00:00')
    updated_at: datetime = Field(..., example='2021-01-01 00:00:00')


class ResponseDetails(BaseModel):
    success: bool = Field(..., example=True)
    details: str = Field(..., example='This is a details message.')
