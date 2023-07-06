import ujson

from typing import Annotated
from fastapi import Depends

from core.cache import MapCacher


class PostLikesCacheRepo:
    TABLE_NAME = "post_likes"

    def __init__(self, cacher: Annotated[MapCacher, Depends()]) -> None:
        self.cacher = cacher

    async def _get_post_data(self, post_id: int) -> list[str]:
        """ Returns post data """
        result = await self.cacher.get_row(self.TABLE_NAME, str(post_id))
        return ujson.loads(result)

    async def clear_cache(self, post_id: int) -> None:
        """ Clears cache """
        await self.cacher.set_row(self.TABLE_NAME, str(post_id), "[]")

    async def get_likes_by_post(self, post_id: int) -> list[int]:
        """ Returns list of likes by post id """
        result = await self._get_post_data(post_id)
        return [int(user_id) for user_id in result]

    async def like_post(self, post_id: int, user_id: int) -> bool:
        """ 
        Likes post 
        
        :param post_id: Post id
        :param user_id: User id
        :return: True if post was liked, False if post was already liked
        """
        likes_str = await self._get_post_data(post_id)
        likes = [int(user_id) for user_id in likes_str]

        if user_id in likes:
            return False
        likes.append(user_id)
        await self.cacher.set_row(self.TABLE_NAME, str(post_id), ujson.dumps(likes))
        return True
