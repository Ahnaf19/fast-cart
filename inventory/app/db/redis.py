import os

import redis.asyncio
from dotenv import load_dotenv
from loguru import logger
from redis_om import get_redis_connection

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
# weirdly .env stores/reads int as str
REDIS_PORT = int(os.getenv("REDIS_PORT", 12538))

params = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "password": REDIS_PASSWORD,
    "decode_responses": True,
}
logger.debug(
    f"""
             Redis Connection Params in FastAPI:
             REDIS_HOST: {REDIS_HOST}
             REDIS_PORT: {REDIS_PORT}
             """
)


def get_redis_om_client():
    """
    Get the Redis client connection.
    """
    return get_redis_connection(**params)


def get_redis_cache_client():
    """
    Get the Redis cache client connection.
    """
    return redis.asyncio.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}", password=REDIS_PASSWORD, encoding="utf8", decode_responses=True
    )


# redis_db = get_redis_om_client()
# logger.debug(f"check redis ping: {redis_db.ping()}")
# logger.debug(f"Redis Connection Params in FastAPI: {redis_db.connection_pool.connection_kwargs}")


if __name__ == "__main__":
    load_dotenv()

    REDIS_HOST = os.getenv("REDIS_HOST")
    # REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 12538))

    params = {
        "host": REDIS_HOST,
        "port": REDIS_PORT,
        "password": REDIS_PASSWORD,
        "decode_responses": True,
    }

    print(params)

    redis_db = get_redis_om_client(**params)
    # logger.debug(f"Redis Connection Params in FastAPI: {redis_db.connection_pool.connection_kwargs}")

    print(redis_db.ping())
