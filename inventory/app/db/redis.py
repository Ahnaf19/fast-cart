import os

import redis.asyncio
from dotenv import load_dotenv
from fastapi_cache.coder import JsonCoder
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


class CustomJsonCoder(JsonCoder):
    """
    A custom JSON coder that extends the functionality of the JsonCoder class
    to ensure proper encoding and decoding of JSON data with UTF-8 support.
    Methods:
        encode(value):
            Encodes the given value into a JSON-compatible format, ensuring
            the result is in bytes if it is a string.
        decode(value):
            Decodes the given value from a JSON-compatible format, ensuring
            it is properly converted from bytes to a string if necessary.
            Raises a TypeError if the value is not a string or bytes.
    """

    @classmethod
    def encode(cls, value):
        encoded_value = super().encode(value)
        if isinstance(encoded_value, str):
            return encoded_value.encode("utf-8")  # Ensure bytes
        return encoded_value

    @classmethod
    def decode(cls, value):
        if isinstance(value, bytes):
            value = value.decode("utf-8")  # Ensure it's a string
        elif not isinstance(value, str):
            raise TypeError("Value must be a string or bytes")
        return super().decode(value.encode("utf-8") if isinstance(value, str) else value)


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

    # print(params)

    redis_db = get_redis_om_client(**params)
    # logger.debug(f"Redis Connection Params in FastAPI: {redis_db.connection_pool.connection_kwargs}")

    print(redis_db.ping())
