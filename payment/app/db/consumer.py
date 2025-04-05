import asyncio

import redis
from loguru import logger

from payment.app.db.postgresql import get_db
from payment.app.db.redis_stream import get_redis_stream_client
from payment.app.services.service import OrderService


async def consume_order_refund(redis_stream_client: redis.client.Redis, key: str, group: str, block_: int = 3000):
    """
    Continuously listens to the Redis stream for refund order events.
    """
    # Product.set_meta_attr(redis_stream_client, global_key_prefix="fastcart", model_key_prefix="inventory.Product")
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
                for message in messages:
                    obj = message[1][0][1]

                    async for session in get_db():
                        order = await OrderService.get_order(obj["order_id"], session)

                        if order:
                            logger.info(f"Fetched order from sql db: {order}")

                            order.order_status = "refunded"

                            await session.commit()
                            await session.refresh(order)

                            logger.info("refunded order successfully")
                        else:
                            logger.error(f"order with ID {obj['order_id']} not found.")

        except Exception as e:
            logger.exception(f"Error consuming Redis stream: {e}")

        await asyncio.sleep(1)  # Prevent busy-waiting


# * Initialize Redis OM client for data operations
redis_stream_client = get_redis_stream_client()
# logger.debug(f"Redis client used in consumer: {redis_stream_client.connection_pool.connection_kwargs}")

key = "refund_order"
group = "payment_group"

try:
    redis_stream_client.xgroup_create(key, group)
except redis.exceptions.RedisError as e:
    logger.info(f"Group '{group}' already exists for stream '{key}'. Error: {e}")


async def consume():
    await consume_order_refund(redis_stream_client, key, group)


if __name__ == "__main__":
    asyncio.run(consume())
