from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from redis_om import HashModel

from inventory.app.db.redis import redis_db


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

    class Config:
        schema_extra = {
            "example": {
                "name": "New Product",
                "price": 34.99,
                "quantity": 30,
                "creation_time": "2023-10-01T12:00:00",
            }
        }


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Updated Product",
                "price": 19.99,
                "quantity": 10,
            }
        }
