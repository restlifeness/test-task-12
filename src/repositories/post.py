
from typing import Annotated
from fastapi import Depends

from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.generic import GenericRepo

from db.models import Post
from db.session import get_session


class PostRepo(GenericRepo[Post]):
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
        self.Model = Post
        super().__init__(session, self.Model)

    async def get_by_id_with_author(self, id: int) -> Post:
        """
        Get post by id with relation.
        
        :param id: Post id.
        :return: Post.
        """
        query = (
            select(self.Model)
            .options(selectinload(Post.author))
            .where(self.Model.id == id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def filter_with_author(self, page: int, limit: int, **kwargs) -> list[Post]:
        """
        Filter posts with relation.
    
        :param page: Page of pagination.
        :param limit: Limit for pagination page.
        :param kwargs: Filter params.
        :return: List of posts.
        """
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        query = (
            select(self.Model)
            .options(selectinload(Post.author))
        )
        if filters:
            query = query.where(and_(*filters))
        query = (
            query
            .order_by(self.Model.created_at.desc())
            .offset(page * limit)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def paginate_with_author(self, page: int, limit: int) -> list[Post]:
        """
        Paginate posts with relation.
    
        :param page: Page of pagination.
        :param limit: Limit for pagination page.
        :return: List of posts.
        """
        query = (
            select(self.Model)
            .options(selectinload(Post.author))
            .order_by(self.Model.created_at.desc())
            .offset(page * limit)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_post_if_author(self, post_id: int, user_id: int, **kwargs) -> bool:
        """
        Update a post only if the given user is the author.

        :param post_id: The ID of the post to update.
        :param user_id: The ID of the user trying to update.
        :param kwargs: The fields to be updated with their new values.
        """
        stmt = update(self.model).where(
            and_(self.model.id == post_id, self.model.author_id == user_id)
        ).values(**kwargs)

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.rowcount > 0


    async def delete_post_if_author(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post only if the given user is the author.

        :param post_id: The ID of the post to delete.
        :param user_id: The ID of the user trying to delete.
        """
        stmt = delete(self.model).where(
            and_(self.model.id == post_id, self.model.author_id == user_id)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.rowcount > 0

    async def set_likes(self, post_id: int, likes: int = 0) -> None:
        """
        Add likes of post.

        :param post_id: Post id.
        """
        stmt = update(self.model).where(self.model.id == post_id).values(
            likes=likes
        )
        await self.session.execute(stmt)
        await self.session.commit()
