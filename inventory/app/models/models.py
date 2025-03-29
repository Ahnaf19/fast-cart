from datetime import datetime

from pydantic import BaseModel, Field
from redis_om import HashModel

from inventory.app.db.redis import redis_db

# from loguru import logger


# logger.debug(f"Redis Connection Params in FastAPI: {redis_db.connection_pool.connection_kwargs}")


class ResponseModel(BaseModel):
    """
    Represents generic response model
    """

    message: str


class Product(HashModel):
    name: str
    price: float
    quantity: int
    # Store timestamp as ISO 8601 string
    creation_time: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Meta:
        # This is the Redis connection
        # for each product it will store a hash in Redis
        database = redis_db
