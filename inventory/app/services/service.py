from loguru import logger

from inventory.app.models.models import Product, UpdateProduct


class Service(Product):
    """
    Service class to handle operations.
    """

    def __init__(self) -> None:
        """
        Initialize the Service.
        """
        logger.debug("Service initialized")

    def get_all_products(self) -> list[dict[str, str | float | int]]:
        """
        Get all products from the database
        """
        # return Product.all_pks()
        return [self.product_format(pk) for pk in Product.all_pks()]

    @staticmethod
    def product_format(pk: str) -> dict[str, str | float | int]:
        product = Product.get(pk)

        return {
            "id": product.pk if product.pk else "not found",
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "creation_time": product.creation_time,
        }

    def add_product(self, product: Product) -> Product:
        """
        Add a product to the database
        """
        logger.debug(product)  # Debugging the serialized data

        # Save the actual product to Redis
        return product.save()

    def get_product_by_pk(self, pk: str) -> dict[str, str | float | int]:
        """
        Get a product by its primary key (pk).
        """
        return self.product_format(pk)

    def update_product_by_pk(self, pk: str, update_product: UpdateProduct) -> Product:
        """
        Update a product by its primary key (pk).
        """
        product = Product.get(pk)
        update_data = update_product.dict(exclude_unset=True)

        product.update(**update_data)

        return product.save()

    def delete_product_by_pk(self, pk: str) -> dict[str, str | float | int]:
        """
        Delete a product by its primary key (pk).
        """
        product = Product.get(pk)
        product_dict = product.dict()

        Product.delete(product.pk)

        return product_dict
