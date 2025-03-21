from fastapi import HTTPException


class CustomNotFoundException(HTTPException):
    """
    Exception raised when data is not found.

    Attributes:
        id (str): ID of the data that was not found.
    """

    def __init__(self, id: str):
        """
        Initialize the CustomNotFoundException with the given ID.

        Args:
            id (str): ID of the data that was not found.
        """
        detail = {
            "error_message": f"data with id {id} not found",
            "id": id,
        }

        super().__init__(status_code=404, detail=detail)
