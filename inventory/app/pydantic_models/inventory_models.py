from db.redis import redis_db
from pydantic import BaseModel
from redis_om import HashModel


class ResponseModel(BaseModel):
    """
    Represents generic response model
    """

    message: str


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        # This is the Redis connection
        # for each product it will store a hash in Redis
        database = redis_db
