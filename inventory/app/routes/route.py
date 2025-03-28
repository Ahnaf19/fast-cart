from fastapi import APIRouter

from inventory.app.models.models import Product, UpdateProduct
from inventory.app.services.service import Service

# Initialize the router with a prefix and tags
router = APIRouter(prefix="/inventory", tags=["inventory"])

# Initiate the Service
inventory_service = Service()


# Define the routes


@router.get("/products", response_model=list[dict[str, str | float | int]])
def get_all_products() -> list[dict[str, str | float | int]]:
    """
    Get all products from the database
    """
    return inventory_service.get_all_products()


@router.get("/product/{pk}", response_model=dict[str, str | float | int])
def get_product(pk: str) -> dict[str, str | float | int]:
    """
    Get a product by its primary key (pk).
    """
    return inventory_service.get_product_by_pk(pk)


@router.post("/product", response_model=Product)
def add_product(product: Product) -> Product:
    """
    Add a product to the database
    """
    return inventory_service.add_product(product)


@router.put("/product/{pk}", response_model=UpdateProduct)
def update_product(pk: str, update_product: UpdateProduct) -> Product:
    """
    Update a product by its primary key (pk).
    """
    return inventory_service.update_product_by_pk(pk, update_product)


@router.delete("/product/{pk}", response_model=dict[str, str | float | int])
def delete_product(pk: str) -> dict[str, str | float | int]:
    """
    Delete a product by its primary key (pk).
    """
    return inventory_service.delete_product_by_pk(pk)
