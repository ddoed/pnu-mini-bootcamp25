from redis import asyncio as aioredis

REDIS_URL = "redis://127.0.0.1"

async def get_redis():
    return await aioredis.from_url(REDIS_URL, decode_responses=True)