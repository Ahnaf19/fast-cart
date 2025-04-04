from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException

from payment.app.db.postgresql import SessionDep
from payment.app.models.models import Order, OrderRequest, UpdateOrder
from payment.app.services.service import OrderService

# import requests


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=Order)
async def create_order(order_req: OrderRequest, session: SessionDep, background_tasks: BackgroundTasks):
    """
    Creates a new order.

    Args:
        order_req (OrderRequest): Order request details [order id and order quantity].
        session (SessionDep): Database session dependency.

    Returns:
        Order: The newly created order.
    """
    order = await OrderService.order_request(order_req, session)

    background_tasks.add_task(OrderService.process_order, order, session)

    return order


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, session: SessionDep):
    """
    Retrieves an order by order_id.

    Args:
        order_id (int): ID of the order.
        session (Session): Database session.

    Returns:
        Order: Found order or raises HTTP 404.
    """
    order = OrderService.get_order(order_id, session)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
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


@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, updated_data: UpdateOrder, session: SessionDep):
    """
    Updates an existing order.

    Args:
        order_id (int): ID of the order to update.
        updated_data (Order): Updated order details.
        session (Session): Database session.

    Returns:
        Order: Updated order or raises HTTP 404.
    """
    order = OrderService.update_order(order_id, updated_data, session)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order


@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, session: SessionDep):
    """
    Deletes an order.

    Args:
        order_id (int): ID of the order.
        session (Session): Database session.

    Returns:
        dict: Confirmation message or raises HTTP 404.
    """
    deleted_order = OrderService.delete_order(order_id, session)
    if not deleted_order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return deleted_order
