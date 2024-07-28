import aioredis

class Caching:
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis = aioredis.from_url(redis_url)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expiry: int):
        await self.redis.set(key, value, ex=expiry)
