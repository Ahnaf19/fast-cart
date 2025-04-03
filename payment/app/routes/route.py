from typing import List

from fastapi import APIRouter, HTTPException

from payment.app.db.postgresql import SessionDep
from payment.app.models.models import Order
from payment.app.services.service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=Order)
def create_order(order: Order, session: SessionDep):
    """
    Creates a new order.

    Args:
        order (Order): Order details.
        session (Session): Database session.

    Returns:
        Order: The newly created order.
    """
    return OrderService.create_order(order, session)


@router.get("/{product_id}", response_model=Order)
def get_order(product_id: str, session: SessionDep):
    """
    Retrieves an order by product_id.

    Args:
        product_id (str): ID of the product.
        session (Session): Database session.

    Returns:
        Order: Found order or raises HTTP 404.
    """
    order = OrderService.get_order(product_id, session)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/", response_model=List[Order])
def get_all_orders(session: SessionDep):
    """
    Retrieves all orders.

    Args:
        session (Session): Database session.

    Returns:
        List[Order]: List of all orders.
    """
    return OrderService.get_all_orders(session)


@router.put("/{product_id}", response_model=Order)
def update_order(product_id: str, updated_data: Order, session: SessionDep):
    """
    Updates an existing order.

    Args:
        product_id (str): ID of the product to update.
        updated_data (Order): Updated order details.
        session (Session): Database session.

    Returns:
        Order: Updated order or raises HTTP 404.
    """
    order = OrderService.update_order(product_id, updated_data, session)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{product_id}", response_model=dict)
def delete_order(product_id: str, session: SessionDep):
    """
    Deletes an order.

    Args:
        product_id (str): ID of the product.
        session (Session): Database session.

    Returns:
        dict: Confirmation message or raises HTTP 404.
    """
    success = OrderService.delete_order(product_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}
