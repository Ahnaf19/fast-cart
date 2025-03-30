from datetime import datetime
from typing import Optional

from loguru import logger
from pydantic import BaseModel, Field
from redis_om import HashModel


class BaseRedisModel(HashModel):
    class Meta:
        database = None  # Will be set dynamically
        global_key_prefix = ""  # Default prefix for all models
        model_key_prefix = "BaseRedisModel"  # Default prefix for the model

    @classmethod
    def set_meta_attr(cls, db, global_key_prefix: str, model_key_prefix: str):
        cls.set_database(db)
        cls.set_prefix(global_key_prefix, model_key_prefix)

    @classmethod
    def set_database(cls, db):
        cls.Meta.database = db

    @classmethod
    def set_prefix(cls, global_key_prefix: str, model_key_prefix: str):
        cls.Meta.global_key_prefix = global_key_prefix
        cls.Meta.model_key_prefix = model_key_prefix


class Product(BaseRedisModel):
    name: str
    price: float
    quantity: int
    # Store timestamp as ISO 8601 string
    creation_time: str = Field(default_factory=lambda: datetime.now().isoformat())

    # class Meta:
    # https://github.com/redis/redis-om-python/blob/main/docs/models.md
    # This is the Redis connection
    # for each product it will store a hash in Redis

    # database = redis_db

    # key structure: {global_key_prefix}:{model_key_prefix}:{primary_key}
    # defaults to :* and {new_class.__module__}.{new_class.__name__}
    # or you can set custom prefix

    # global_key_prefix = "fastcart"
    # model_key_prefix = "inventory"

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


def _migrate_keys(
    redis_client,
    OLD_PREFIX: str = ":inventory.app.models.models.Product",
    NEW_PREFIX: str = ":Product",
) -> None:
    """
    Migrate Redis hash keys from an old naming convention to a new one.
    This function scans Redis for keys matching the old prefix, extracts the
    unique identifier from each key, and creates a new key using the new prefix.
    The hash data associated with the old key is copied to the new key, and the
    old key is deleted after the migration.
    Args:
        OLD_PREFIX (str): The prefix of the old Redis keys to be migrated.
                          Defaults to ":inventory.app.models.models.Product".
        NEW_PREFIX (str): The prefix for the new Redis keys. Defaults to ":Product".
        redis_client: The Redis client instance used to interact with the Redis database.
    Returns:
        None
    """

    cursor = 0
    while True:
        # Scan for keys with the old prefix
        cursor, keys = redis_client.scan(cursor, match=f"{OLD_PREFIX}:*")

        for old_key in keys:
            product_id = old_key.split(":")[-1]  # Extract ID from the old key
            new_key = f"{NEW_PREFIX}:{product_id}"  # New key format

            logger.info(f"Migrating {old_key} → {new_key}")

            # Copy hash data
            product_data = redis_client.hgetall(old_key)
            redis_client.hset(new_key, mapping=product_data)

            logger.info(f"Product data: {product_data}")

            # Delete old key after copying
            redis_client.delete(old_key)

            logger.info(f"Migrated {old_key} → {new_key}")

        # If scan is complete, break
        if cursor == 0:
            break


if __name__ == "__main__":
    # _migrate_keys()
    print("models.py ran successfully")
