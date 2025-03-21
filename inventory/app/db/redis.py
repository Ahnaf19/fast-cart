import os

from dotenv import load_dotenv
from redis_om import get_redis_connection

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
# weirdly .env stores int as str
REDIS_PORT = int(os.getenv("REDIS_PORT", 12538))

params = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "password": REDIS_PASSWORD,
    "decode_responses": True,
}

redis_db = get_redis_connection(**params)

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

    print(redis_db.ping())
