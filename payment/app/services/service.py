import requests
from fastapi import HTTPException

# from loguru import logger
from sqlalchemy import Numeric, cast, update
from sqlmodel import select

from payment.app.db.postgresql import SessionDep
from payment.app.models.models import Order, OrderRequest, UpdateOrder


class OrderService:
    """
    Handles Order business logic.
    """

    @staticmethod
    async def order_request(order_req: OrderRequest, session: SessionDep) -> Order:
        """
        Creates a new order request and persists it in the database.

        Args:
            order_req (OrderRequest): An object containing the details of the order request,
                                      including order ID and quantity.
            session (SessionDep): The database session dependency for interacting with the database.

        Returns:
            Order: The created Order object with details such as product ID, price, fee, total,
                   quantity, and status.

        Raises:
            requests.exceptions.RequestException: If there is an issue with the HTTP request
                                                  to the inventory service.
            KeyError: If the expected keys are missing in the response from the inventory service."""

        order_req_dict = order_req.model_dump()

        req = requests.get(f"http://127.0.0.1:8000/inventory/product/{order_req_dict['product_id']}", timeout=10)
        product = req.json()

        # Validate order quantity against product quantity
        if int(order_req_dict["order_quantity"]) > int(product["quantity"]):
            raise HTTPException(
                status_code=400,
                detail=f"""
                Requested quantity ({order_req_dict['order_quantity']})
                : exceeds available stock ({product['quantity']}).""",
            )

        # TODO: fix the data validation of inventorty/product/{pk} response to get rid of manual formatting
        order = Order(
            product_id=product["id"],
            price=float(product["price"]),
            fee_per_unit=0.2 * float(product["price"]),
            total=1.2 * float(product["price"]) * int(order_req_dict["order_quantity"]),
            order_quantity=int(order_req_dict["order_quantity"]),
            status="pending",
        )

        return await OrderService.create_order(order, session)

    @staticmethod
    async def create_order(order: Order, session: SessionDep) -> Order:
        """
        Creates a new order in the database.

        Args:
            order (Order): Order object to be added.
            session (Session): Database session.

        Returns:
            Order: The newly created order.
        """
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order

    @staticmethod
    async def get_order(order_id: int, session: SessionDep) -> Order | None:
        """
        Retrieves an order by order_id.

        Args:
            order_id (int): ID of the order.
            session (Session): Database session.

        Returns:
            Order | None: Found order or None.
        """
        return await session.get(Order, order_id)

        # * used to initiate redis stream key
        # order = await session.get(Order, order_id)
        # logger.debug(order)
        # redis_stream_client = get_redis_stream_client()
        # if order is None:
        #     raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
        # redis_stream_client.xadd('refund_order', order.model_dump(), id='*')

        # return order

    @staticmethod
    async def get_all_orders(session: SessionDep) -> list[Order]:
        """
        Retrieves all orders from the database.

        Args:
            session (Session): Database session.

        Returns:
            list[Order]: List of all orders.
        """
        return list((await session.exec(select(Order))).all())

    @staticmethod
    async def update_order(order_id: int, updated_data: UpdateOrder, session: SessionDep) -> Order | None:
        """
        Updates an order with new data using `update()` for efficiency.

        Args:
            order_id (int): ID of the order to update.
            updated_data (UpdateOrder): Updated order data.
            session (Session): Database session.

        Returns:
            Order: The updated order.

        Raises:
            ValueError: If the order with the given order_id does not exist.
        """
        update_data = updated_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update.")

        # Ensure the order exists before updating
        existing_order = (await session.exec(select(Order).where(Order.order_id == order_id))).first()
        if not existing_order:
            raise ValueError(f"Order with id '{order_id}' not found.")

        # Run update query directly
        stmt = (
            update(Order)
            .where(cast(Order.order_id, Numeric) == order_id)
            .values(**update_data)
            .returning(Order)  # Return the updated row
        )
        _ = await session.execute(stmt)
        await session.commit()

        updated_order = (await session.exec(select(Order).where(Order.order_id == order_id))).first()

        return updated_order

    @staticmethod
    async def delete_order(order_id: int, session: SessionDep) -> dict | None:
        """
        Deletes an order by order_id.

        Args:
            order_id (int): ID of the order to delete.
            session (Session): Database session.

        Returns:
            dict: order dict if found and deleted successfully, None otherwise.
        """
        order = await session.get(Order, order_id)
        order_dict = order.model_dump() if order else None
        if not order:
            raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")

        await session.delete(order)
        await session.commit()
        return order_dict
