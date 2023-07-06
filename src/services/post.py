
from typing import Annotated
from fastapi import Depends

from db.models import Post
from core.settings import get_settings

from repositories.post import PostRepo
from repositories.post_cache import PostLikesCacheRepo
from repositories.like import LikeRepo

from schemas.post import PostCreate, PostUpdate


settings = get_settings()


class PostService:
    def __init__(
        self, 
        post_repo: Annotated[PostRepo, Depends()],
        post_likes_cache_repo: Annotated[PostLikesCacheRepo, Depends()],
        like_repo: Annotated[LikeRepo, Depends()],
    ) -> None:
        self.post_repo = post_repo
        self.likes_cache = post_likes_cache_repo
        self.like_repo = like_repo

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

    async def _update_likes_counter(self, post_id: int,) -> None:
        """ Update likes counter """
        likes = await self.like_repo.get_all_likes_by_post(post_id)
        await self.post_repo.set_likes(post_id, len(likes))

    async def _sync_likes(self, post_id: int) -> None:
        """ Sync likes """
        likes = await self.likes_cache.get_likes_by_post(post_id)

        likes_db = await self.like_repo.get_all_likes_by_post(post_id)
        likes_db = [like.user_id for like in likes_db]

        for user_id in likes:
            if user_id in likes_db:
                continue
            await self.like_repo.create_like(post_id, user_id)
        await self._update_likes_counter(post_id)

    async def like_post(self, post_id: int, user_id: int) -> None:
        """ Like post """
        await self.likes_cache.like_post(post_id, user_id)
        
        cache_likes = await self.likes_cache.get_likes_by_post(post_id)
        if len(cache_likes) >= settings.POST_LIKES_CACHE_THRESHOLD:
            await self._sync_likes(post_id)
            await self.likes_cache.clear_cache(post_id)
