
from typing import Annotated
from fastapi import Depends

from db.models import Post

from repositories.post import PostRepo
from schemas.post import PostCreate, PostUpdate

class PostService:
    def __init__(self, post_repo: Annotated[PostRepo, Depends()]) -> None:
        self.post_repo = post_repo

    async def create_post(self, post_data: PostCreate, author_id: int) -> Post:
        """ Create post """
        post = await self.post_repo.create(
            **post_data.dict(),
            author_id=author_id,
        )
        return post

    async def update_post(self, post_data: PostUpdate, author_id: int) -> Post:
        """ Update post """
        post = await self.post_repo.update(
            **post_data.dict(),
            author_id=author_id,
        )
        return post

    async def like_post(self, post_id: int, user_id: int) -> None:
        """ Like post """
        pass
