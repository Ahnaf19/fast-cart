from sqlalchemy import Numeric, cast, update
from sqlmodel import select

from payment.app.db.postgresql import SessionDep
from payment.app.models.models import Order, UpdateOrder

# from loguru import logger


class OrderService:
    """
    Handles Order business logic.
    """

    @staticmethod
    def create_order(order: Order, session: SessionDep) -> Order:
        """
        Creates a new order in the database.

        Args:
            order (Order): Order object to be added.
            session (Session): Database session.

        Returns:
            Order: The newly created order.
        """
        session.add(order)
        session.commit()
        session.refresh(order)  # Refresh to get updated data
        return order

    @staticmethod
    def get_order(product_id: str, session: SessionDep) -> Order | None:
        """
        Retrieves an order by product_id.

        Args:
            product_id (str): ID of the product.
            session (Session): Database session.

        Returns:
            Order | None: Found order or None.
        """
        return session.get(Order, product_id)

    @staticmethod
    def get_all_orders(session: SessionDep) -> list[Order]:
        """
        Retrieves all orders from the database.

        Args:
            session (Session): Database session.

        Returns:
            list[Order]: List of all orders.
        """
        return list(session.exec(select(Order)).all())

    @staticmethod
    def update_order(product_id: str, updated_data: UpdateOrder, session: SessionDep) -> Order:
        """
        Updates an order with new data using `update()` for efficiency.

        Args:
            product_id (str): ID of the product to update.
            updated_data (UpdateOrder): Updated order data.
            session (Session): Database session.

        Returns:
            Order: The updated order.

        Raises:
            ValueError: If the order with the given product_id does not exist.
        """
        update_data = updated_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update.")

        # Ensure the order exists before updating
        existing_order = session.exec(select(Order).where(Order.product_id == product_id)).first()
        if not existing_order:
            raise ValueError(f"Order with product_id '{product_id}' not found.")

        # Run update query directly
        stmt = (
            update(Order)
            .where(cast(Order.product_id, Numeric) == product_id)
            .values(**update_data)
            .returning(Order)  # Return the updated row
        )
        result = session.execute(stmt)
        session.commit()

        return result.scalar_one()  # Assumes the update succeeded

    @staticmethod
    def delete_order(product_id: str, session: SessionDep) -> bool:
        """
        Deletes an order by product_id.

        Args:
            product_id (str): ID of the product to delete.
            session (Session): Database session.

        Returns:
            bool: True if deleted, False if not found.
        """
        order = session.get(Order, product_id)
        if not order:
            return False

        session.delete(order)
        session.commit()
        return True
