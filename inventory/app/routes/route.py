from fastapi import APIRouter

from inventory.app.pydantic_models.inventory_models import Product
from inventory.app.services.service import Service

# Initialize the router with a prefix and tags
router = APIRouter(prefix="/inventory", tags=["inventory"])

# Initiate the Service
guest_service = Service()


# Define the routes
# @router.get("/", response_model=ResponseModel)
# async def read_data() -> ResponseModel:
#     """
#     Retrieve all data.

#     Returns:
#         ResponseModel: A list of all data.
#     """
#     response = {"message": "ok"}
#     return ResponseModel(**response)


@router.get("/products")
def get_all_products():
    """
    Get all products from the database
    """
    return Product.all_pks()
