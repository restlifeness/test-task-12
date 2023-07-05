
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.jwt import decode_token

from db.models import User
from repositories.user import UserRepo


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_by_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: Annotated[UserRepo, Depends()]
) -> User:
    """
    Get a user by token.

    Args:
        token (str): The JWT token.
        user_service (UserService): The user service.

    Returns:
        User: The user.
    """
    payload = decode_token(token=token)
    username: str = payload.get("username", None)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repo.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
