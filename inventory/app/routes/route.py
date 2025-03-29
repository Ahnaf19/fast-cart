from fastapi import APIRouter

from inventory.app.models.models import Product
from inventory.app.services.service import Service

# Initialize the router with a prefix and tags
router = APIRouter(prefix="/inventory", tags=["inventory"])

# Initiate the Service
inventory_service = Service()


# Define the routes


@router.get("/products")
def get_all_products():
    """
    Get all products from the database
    """
    return inventory_service.get_all_products()


@router.get("/products/{pk}")
def get_product(pk: str):
    """
    Get a product by its primary key (pk).
    """
    return inventory_service.get_product_by_pk(pk)


@router.post("/products")
def add_product(product: Product):
    """
    Add a product to the database
    """
    # return product.save()
    return inventory_service.add_product(product)


@router.delete("/products/{pk}")
def delete_product(pk: str):
    """
    Delete a product by its primary key (pk).
    """
    return inventory_service.delete_product_by_pk(pk)
