import os
import redis
from fastapi import Request, HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis.from_url(REDIS_URL)

RATE_LIMIT = int(os.getenv("RATE_LIMIT")) # max requests
TIME_WINDOW =int(os.getenv("TIME_WINDOW"))  # in seconds

async def rate_limiter(request: Request):
    ip = request.client.host
    key = f"rate-limit:{ip}"

    current = redis_client.get(key)
    
    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )
    
    pipeline = redis_client.pipeline()
    pipeline.incr(key, 1)
    pipeline.expire(key, TIME_WINDOW)
    pipeline.execute()
