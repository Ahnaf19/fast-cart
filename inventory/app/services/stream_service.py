from inventory.app.db.redis import get_redis_stream_client

# from payment.app.models.models import Order


class StreamService:
    """
    Service for handling Redis stream operations related to orders.
    """

    @staticmethod
    def stream_order_refund(obj: dict) -> None:
        """
        Adds a completed order to the Redis stream.

        Args:
            order (Order): Order object to be added to the stream.

        Returns:
            None
        """
        redis_stream = get_redis_stream_client()
        redis_stream.xadd(name="refund_order", fields=obj, id="*")
