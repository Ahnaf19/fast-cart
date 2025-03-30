from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
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

    @cache(namespace="inventory.products", expire=600)  # Cache for 10 mins
    async def get_all_products(self) -> list[dict[str, str | float | int]]:
        """
        Get all products from the database
        """
        # return Product.all_pks()
        return [result for pk in Product.all_pks() if isinstance((result := await self.product_format(pk)), dict)]

    @staticmethod
    # @cache(namespace="inventory.product", expire=120)  # Cache for 2 mins
    async def product_format(pk: str) -> dict[str, str | float | int]:
        product = Product.get(pk)

        return {
            "id": product.pk if product.pk else "not found",
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "creation_time": product.creation_time,
        }

    async def add_product(self, product: Product) -> Product:
        """
        Add a product to the database
        """
        logger.debug(product)

        # Save the actual product to Redis
        product.save()

        await FastAPICache.clear(namespace="inventory.products")

        return product

    @cache(namespace="inventory.product", expire=600)  # Cache for 10 mins
    async def get_product_by_pk(self, pk: str) -> dict[str, str | float | int]:
        """
        Get a product by its primary key (pk).
        """
        result = await self.product_format(pk)
        if isinstance(result, dict):
            return result
        raise TypeError("Expected a dictionary but got a different type.")

    async def update_product_by_pk(self, pk: str, update_product: UpdateProduct) -> Product:
        """
        Update a product by its primary key (pk).
        """
        product = Product.get(pk)
        update_data = update_product.dict(exclude_unset=True)

        product.update(**update_data)

        product.save()

        await FastAPICache.clear(namespace="inventory.products")
        # ! following line is clearing the cache for all products.
        # TODO: for particular product, need to find a way to set and use the correct cache key
        await FastAPICache.clear(namespace="inventory.product", key=pk)

        return product

    async def delete_product_by_pk(self, pk: str) -> dict[str, str | float | int]:
        """
        Delete a product by its primary key (pk).
        """
        product = Product.get(pk)
        product_dict = product.dict()

        Product.delete(product.pk)

        # After deleting, clear the cache for this product
        await FastAPICache.clear(namespace="inventory.products")
        await FastAPICache.clear(namespace="inventory.product", key=pk)

        return product_dict
