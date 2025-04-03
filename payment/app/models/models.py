import datetime

# import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):  # type: ignore
    # `table=True` makes it a database table
    """
    Represents an order in the system.
    """
    # * auto-incrementing primary key, handled by SQLModel
    # * using int for simplicity, but can be changed to UUID if needed
    order_id: Optional[int] = Field(default=None, primary_key=True, index=True, description="Unique order ID")
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

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "12345",
                "price": 19.99,
                "fee": 1.99,
                "total": 21.98,
                "quantity": 2,
                "status": "pending",
            }
        }


class UpdateOrder(SQLModel):
    """
    Represents an update to an existing order.
    """

    product_id: Optional[str] = Field(None, description="Unique identifier for the product")
    price: Optional[float] = Field(None, description="Price of the product")
    fee: Optional[float] = Field(None, description="Fee for the product")
    total: Optional[float] = Field(None, description="Total amount for the product")
    quantity: Optional[int] = Field(None, description="Quantity of the product")
    status: Optional[str] = Field(None, description="Status of the order (e.g., pending, completed)")

    class Config:
        json_schema_extra = {
            "examples": [
                {"product_id": "101", "price": 99.99, "fee": 4.99, "total": 104.98, "quantity": 1, "status": "pending"},
                {
                    "product_id": 202,
                    "price": "50.5",  # Demonstrating conversion from string to float
                    "fee": 2.5,
                    "total": 53.0,
                    "quantity": 2,
                    "status": "completed",
                },
                {
                    "product_id": 303,
                    "price": "invalid_price",  # Invalid data example
                    "fee": "NaN",
                    "total": None,
                    "quantity": "five",
                    "status": "unknown",
                },
            ]
        }
