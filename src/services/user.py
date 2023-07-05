
from typing import Annotated
from fastapi import Depends
from werkzeug.security import generate_password_hash, check_password_hash

from db.models import User

from core.settings import get_settings
from core.jwt import create_token

from repositories.user import UserRepo
from schemas.auth import Token
from schemas.user import UserSignUp


settings = get_settings()

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


class UserService:
    def __init__(self, user_repo: Annotated[UserRepo, Depends()]) -> None:
        self.user_repo = user_repo

    def create_access_token(username: str) -> Token:
        """ Create access token for user """
        return Token(
            access_token=create_token({'username': username}),
            token_type='bearer',
        )

    async def auth_user(self, username: str, password: str) -> User | bool:
        """ 
        Authenticate user by username and password
        
        Returns:
            User: User object if user is authenticated
            bool: False if user is not authenticated
        """
        user = await self.user_repo.get_by_username(username)
        if user is None:
            return False
        result = check_password_hash(user.hashed_password, password)
        if not result:
            return False
        return user

    async def create_user(self, user_data: UserSignUp) -> User:
        """ Create user """
        hashed_password = generate_password_hash(user_data.password)

        user = await self.user_repo.create(
            **user_data.dict(),
            hashed_password=hashed_password,
        )
        return user

