from pydantic import BaseModel


class ResponseModel(BaseModel):
    """
    Represents generic response model
    """

    message: str
