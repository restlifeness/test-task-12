
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from services.user import UserService
from schemas.user import UserSignUp, UserOut


user_router = APIRouter(
    tags=['user'],
)


@user_router.post('/signup', response_model=UserOut)
async def create_user(
    user_data: UserSignUp,
    user_service: Annotated[UserService, Depends()]
) -> UserOut:
    """ Create user """
    user = await user_service.create_user(user_data)
    return user
