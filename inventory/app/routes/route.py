from fastapi import APIRouter

from inventory.app.pydantic_models.inventory_models import Product
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


@router.post("/products")
def add_product(product: Product):
    """
    Add a product to the database
    """
    return inventory_service.add_product(product)
