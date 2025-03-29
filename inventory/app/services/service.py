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
        # return Product.all_pks()
        return [self.product_format(pk) for pk in Product.all_pks()]

    def product_format(self, pk: str):
        product = Product.get(pk)

        return {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "creation_time": product.creation_time,
        }

    def add_product(self, product: Product):
        """
        Add a product to the database
        """
        # logger.debug(product)  # Debugging the serialized data

        # Save the actual product (not the dictionary) to Redis
        return product.save()

    def get_product(self, pk: str):
        """
        Get a product by its primary key (pk).
        """
        return self.product_format(pk)
