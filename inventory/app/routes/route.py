from fastapi import APIRouter

from inventory.app.models.models import Product, UpdateProduct
from inventory.app.services.service import Service

# Initialize the router with a prefix and tags
router = APIRouter(prefix="/inventory", tags=["inventory"])

# Initiate the Service
inventory_service = Service()


# Define the routes


@router.get("/products", response_model=list[dict[str, str | float | int]])
async def get_all_products() -> list[dict[str, str | float | int]]:
    """
    Get all products from the database
    """
    products = await inventory_service.get_all_products()
    if isinstance(products, list):
        return list(products)
    raise TypeError("Expected a list of products, but got a non-iterable response.")


@router.get("/product/{pk}", response_model=dict[str, str | float | int])
async def get_product(pk: str) -> dict[str, str | float | int]:
    """
    Get a product by its primary key (pk).
    """
    product = await inventory_service.get_product_by_pk(pk)
    if isinstance(product, dict):
        return product
    raise TypeError("Expected a dictionary, but got a different response type.")


@router.post("/product", response_model=Product)
async def add_product(product: Product) -> Product:
    """
    Add a product to the database
    """
    return await inventory_service.add_product(product)


@router.put("/product/{pk}", response_model=UpdateProduct)
async def update_product(pk: str, update_product: UpdateProduct) -> Product:
    """
    Update a product by its primary key (pk).
    """
    return await inventory_service.update_product_by_pk(pk, update_product)


@router.delete("/product/{pk}", response_model=dict[str, str | float | int])
async def delete_product(pk: str) -> dict[str, str | float | int]:
    """
    Delete a product by its primary key (pk).
    """
    return await inventory_service.delete_product_by_pk(pk)
