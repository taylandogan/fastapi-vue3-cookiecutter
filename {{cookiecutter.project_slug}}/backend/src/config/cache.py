import logging
from typing import Any, Optional

from redis import asyncio as redis
from redis.asyncio.client import Redis


class Cache:
    def __init__(self, url: str) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.cache: Redis = None  # type: ignore
        self.connect(url)

    def connect(self, url: str) -> Redis:
        if not self.cache:
            self.cache = redis.Redis.from_url(url)

        return self.cache

    async def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        value = await self.cache.get(name=key) or default
        value = value.decode() if value else value
        self.logger.debug(f"get {key=}, {value=}, {default=}")
        return value

    async def set(self, key: str, value: str, expire: Optional[int] = None) -> None:
        await self.cache.set(name=key, value=value, ex=expire)
        self.logger.debug(f"set {key=}, {value=}, {expire=}")

    async def delete(self, key: str) -> None:
        await self.cache.delete(key)
        self.logger.debug(f"delete {key=}")
