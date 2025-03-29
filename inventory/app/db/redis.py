import os

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

redis_db = get_redis_connection(**params)
logger.debug(f"check redis ping: {redis_db.ping()}")
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

    redis_db = get_redis_connection(**params)
    # logger.debug(f"Redis Connection Params in FastAPI: {redis_db.connection_pool.connection_kwargs}")

    print(redis_db.ping())
