
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from services.user import UserService
from schemas.auth import Token


auth_router = APIRouter(
    tags=['auth'],
)


@auth_router.post('/token', response_model=Token)
async def auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends()]
) -> Token:
    user = await user_service.auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    token = UserService.create_access_token(user.username)

    return token
