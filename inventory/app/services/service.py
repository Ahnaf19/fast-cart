from loguru import logger

from inventory.app.pydantic_models.inventory_models import Product


class Service(Product):
    """
    Service class to handle operations.
    """

    def __init__(self) -> None:
        """
        Initialize the Service.
        """
        logger.debug("Service initialized")

    def get_all_products(self):
        """
        Get all products from the database
        """
        return self.all_pks()

    def add_product(self, product: Product):
        """
        Add a product to the database
        """
        # Convert to a dictionary (this is for inspection, not saving)
        # product_dict = product.dict()
        logger.debug(product)  # Debugging the serialized data

        # Save the actual product (not the dictionary) to Redis
        product.save()

        # Return the product id
        return {"product_id": product.pk}
