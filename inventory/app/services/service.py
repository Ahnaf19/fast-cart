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

    def get_all_products(self):
        """
        Get all products from the database
        """
        # return Product.all_pks()
        return [self.product_format(pk) for pk in Product.all_pks()]

    @staticmethod
    def product_format(pk: str):
        product = Product.get(pk)

        return {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "creation_time": product.creation_time if product.creation_time else None,
        }

    def add_product(self, product: Product):
        """
        Add a product to the database
        """
        logger.debug(product)  # Debugging the serialized data

        # Save the actual product to Redis
        return product.save()

    def get_product_by_pk(self, pk: str):
        """
        Get a product by its primary key (pk).
        """
        return self.product_format(pk)

    def update_product_by_pk(self, pk: str, update_product: UpdateProduct):
        """
        Update a product by its primary key (pk).
        """
        product = Product.get(pk)
        # product.name = update_product.name
        # product.price = update_product.price
        # product.quantity = update_product.quantity

        update_data = update_product.dict(exclude_unset=True)

        product.update(**update_data)

        return product.save()

    def delete_product_by_pk(self, pk: str):
        """
        Delete a product by its primary key (pk).
        """
        product = Product.get(pk)
        product_dict = product.dict()

        Product.delete(product.pk)

        return product_dict
