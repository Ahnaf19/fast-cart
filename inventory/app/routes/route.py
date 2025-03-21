from app.services.service import Service
from fastapi import APIRouter

from inventory.app.pydantic_models.inventory_models import ResponseModel

# Initialize the router with a prefix and tags
router = APIRouter(prefix="/group", tags=["group"])

# Initiate the Service
guest_service = Service()


# Define the routes
@router.get("/", response_model=ResponseModel)
async def read_data() -> ResponseModel:
    """
    Retrieve all data.

    Returns:
        ResponseModel: A list of all data.
    """
    response = {"message": "ok"}
    return ResponseModel(**response)
