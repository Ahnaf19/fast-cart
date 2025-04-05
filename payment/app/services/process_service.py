import time

from sqlmodel import select

from payment.app.db.postgresql import SessionDep
from payment.app.models.models import Order
from payment.app.services.stream_service import StreamService


class ProcessService:

    @staticmethod
    async def process_order(order: Order, session: SessionDep):
        """
        Processes an order by updating its status to 'completed'.

        Args:
            order (Order): Order object to be processed.
            session (Session): Database session.

        Returns:
            Order: The processed order with updated status.
        """
        # Fetch order again from DB to attach it to the session
        fetched_new_order = (
            await session.exec(select(Order).where(Order.order_id == order.model_dump()["order_id"]))
        ).first()

        if not fetched_new_order:
            raise ValueError("Order not found")  # Handle case where order was deleted

        await asyncio.sleep(5)  # Simulate processing time
        fetched_new_order.status = "completed"
        await session.commit()
        await session.refresh(fetched_new_order)
        # return fetched_new_order

        # * redis stream
        StreamService.stream_order_completed(fetched_new_order)
