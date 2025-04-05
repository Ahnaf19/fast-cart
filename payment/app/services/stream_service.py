from payment.app.db.redis_stream import get_redis_stream_client
from payment.app.models.models import Order


class StreamService:
    """
    Service for handling Redis stream operations related to orders.
    """

    @staticmethod
    def stream_order_completed(order: Order) -> None:
        """
        Adds a completed order to the Redis stream.

        Args:
            order (Order): Order object to be added to the stream.

        Returns:
            None
        """
        redis_stream = get_redis_stream_client()
        redis_stream.xadd(name="order_completed", fields=order.model_dump(), id="*")
