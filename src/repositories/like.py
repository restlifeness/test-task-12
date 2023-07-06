
from typing import Annotated
from fastapi import Depends

from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.generic import GenericRepo

from db.models import UserLike
from db.session import get_session


class LikeRepo(GenericRepo[UserLike]):
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
        self.Model = UserLike
        super().__init__(session, self.Model)

    async def create_like(self, post_id: int, user_id: int) -> UserLike:
        """
        Create like for post.

        :param post_id: Post id.
        :param user_id: User id.
        :return: Like.
        """
        like = UserLike(post_id=post_id, user_id=user_id)
        self.session.add(like)
        await self.session.commit()
        return like

    async def get_all_likes_by_post(self, post_id: int) -> list[UserLike]:
        """
        Get all likes by post.

        :param post_id: Post id.
        :return: List of likes.
        """
        query = select(self.Model).where(self.Model.post_id == post_id)
        result = await self.session.execute(query)
        return result.scalars().all()
