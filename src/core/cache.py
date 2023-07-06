from redis import asyncio as aioredis

from typing import Optional

from core.settings import get_settings


settings = get_settings()

redis = aioredis.from_url(settings.get_redis_uri())


class MapCacher:
    def __init__(self) -> None:
        self.uri = settings.get_redis_uri()

    def _decode_table(self, map: dict[bytes, bytes]) -> dict[str, str]:
        """ Decodes table from bytes to str """
        return {k.decode(): v.decode() for k, v in map.items()}

    def _decode_row(self, row: bytes) -> str:
        """ Decodes row from bytes to str """
        return row.decode()

    async def create_table(self, table: str, map: dict[str, str]) -> None:
        """ Creates table if it does not exist """
        await redis.hmset(table, map)

    async def get_table(self, table: str) -> dict[str, str]:
        """ Returns empty dict if table does not exist """
        result = await redis.hgetall(table)
        if not result:
            return {}
        return self._decode_table(result)

    async def get_row(self, table: str, row: str) -> str:
        """ Returns None if row does not exist """
        row = await redis.hget(table, row)
        if not row:
            return "[]"
        return self._decode_row(row)

    async def set_row(self, table: str, row: str, value: str) -> None:
        """ Creates row if it does not exist """
        await redis.hset(table, row, value)
