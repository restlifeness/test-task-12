
from typing import Annotated
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.generic import GenericRepo

from db.models import User
from db.session import get_session



class UserRepo(GenericRepo[User]):
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
        self.Model = User
        super().__init__(session, self.Model)

    async def get_by_username(self, username: str) -> User:
        result = await self.session.execute(select(self.Model).where(self.Model.username == username))
        return result.scalar_one_or_none()
