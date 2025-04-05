import asyncio

import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger

from inventory.app.db.redis import CustomJsonCoder, get_redis_cache_client, get_redis_om_client
from inventory.app.main import app
from inventory.app.models.models import Product
from inventory.app.services.stream_service import StreamService
from inventory.app.services.utils import clear_cache_by_pk


def get_redis_stream_client():
    """
    Retrieves the Redis stream client initialized in the FastAPI app.
    """
    try:
        logger.debug("using app.state.redis")
        return app.state.redis  # Reuse the existing Redis connection
    except AttributeError:
        logger.debug("app.state.redis not found. using fresh get_redis_om_client")
        return get_redis_om_client()  # Fallback to the default Redis connection


async def consume_order_completed(redis_stream_client: redis.client.Redis, key: str, group: str, block_: int = 3000):
    """
    Continuously listens to the Redis stream for completed order events.
    """
    Product.set_meta_attr(redis_stream_client, global_key_prefix="fastcart", model_key_prefix="inventory.Product")
    while True:
        try:
            # * Read new messages from Redis stream (blocking for 5 sec if no messages)
            messages = redis_stream_client.xreadgroup(group, key, {key: ">"}, block=block_)
            logger.info(f"Received messages: {messages}")

            # for stream, message_list in messages:
            #     for message_id, message_data in message_list:
            #         logger.info(f"Received order completed event: {message_data}")
            # Process the message (e.g., update inventory, trigger further workflows)

            if messages != []:
                message_list = messages[0][1]
                for message in message_list:
                    obj = message[1]
                    product = Product.get(obj["product_id"])

                    if product:
                        logger.info(f"Product: {product}")
                        logger.debug(product.key())

                        product.quantity -= int(obj["order_quantity"])
                        product.save()
                        await FastAPICache.clear(namespace="inventory.products")
                        await clear_cache_by_pk(pk=obj["product_id"], namespace="inventory.product")

                        logger.info("Updated product quantity successfully")
                    else:
                        logger.error(f"Product with ID {obj['product_id']} not found.")
                        StreamService.stream_order_refund(obj)

        except Exception as e:
            logger.exception(f"Error consuming Redis stream: {e}")

        await asyncio.sleep(1)  # Prevent busy-waiting


# * Initialize Redis OM client for data operations
redis_stream_client = get_redis_stream_client()
# logger.debug(f"Redis client used in consumer: {redis_stream_client.connection_pool.connection_kwargs}")

# * Initialize Redis client for caching, set coder for reading from cache
global redis_cache
redis_cache = get_redis_cache_client()
FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache", coder=CustomJsonCoder)

key = "order_completed"
group = "inventory_group"

try:
    redis_stream_client.xgroup_create(key, group)
except redis.exceptions.RedisError as e:
    logger.info(f"Group '{group}' already exists for stream '{key}'. Error: {e}")


async def consume():
    await consume_order_completed(redis_stream_client, key, group)


if __name__ == "__main__":
    asyncio.run(consume())
