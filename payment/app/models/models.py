import datetime

# import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):  # type: ignore
    # `table=True` makes it a database table
    """
    Represents an order in the system.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True, description="Unique order ID")
    # id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, description="Unique order ID")
    product_id: str = Field(index=True, description="Unique identifier for the product")
    price: float = Field(..., description="Price of the product")
    fee: float = Field(..., description="Fee for the product")
    total: float = Field(..., description="Total amount for the product")
    quantity: int = Field(..., description="Quantity of the product")
    status: str = Field(..., description="Status of the order (e.g., pending, completed)")
    created_at: str = Field(
        default_factory=lambda: datetime.datetime.now().isoformat(), description="Timestamp when the order was created"
    )


class UpdateOrder(SQLModel):
    """
    Represents an update to an existing order.
    """

    product_id: Optional[int] = Field(None, description="Unique identifier for the product")
    price: Optional[float] = Field(None, description="Price of the product")
    fee: Optional[float] = Field(None, description="Fee for the product")
    total: Optional[float] = Field(None, description="Total amount for the product")
    quantity: Optional[int] = Field(None, description="Quantity of the product")
    status: Optional[str] = Field(None, description="Status of the order (e.g., pending, completed)")
