from typing import Optional

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from inventory.app.models.models import Product


def product_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    *args,
    **kwargs,
):
    # https://github.com/long2ice/fastapi-cache/blob/main/fastapi_cache/decorator.py
    # https://pypi.org/project/fastapi-cache2/0.2.0/

    # logger.debug(f"key builder Args: {args}")
    logger.debug(f"key builder Kwargs: {kwargs}")

    # Try to find pk in different places
    pk = kwargs.get("pk")  # Check kwargs
    if not pk and "args" in kwargs and len(kwargs["args"]) > 1:
        pk = kwargs["args"][1]  # Extract from args tuple

    if pk:
        catche_key = f"{namespace}:{pk}"
        logger.debug(f"Cache key: {catche_key}")
        return catche_key

    raise ValueError("Cache key builder error: No primary key (pk) provided.")


async def clear_cache_by_namespace(namespace: str) -> None:
    """
    Clears the cache for a specific namespace or the entire cache if the namespace is empty.

    Args:
        namespace (str): The namespace to clear from the cache. If an empty string is provided,
                         the entire cache will be cleared.

    Raises:
        Exception: If an error occurs during the cache clearing process.

    Notes:
        This function uses the FastAPICache library to interact with the cache backend.
        The cache key is constructed using the prefix and the provided namespace.
    """
    prefix = FastAPICache.get_prefix()
    cache_backend = FastAPICache.get_backend()

    if not isinstance(cache_backend, RedisBackend):
        raise TypeError("Cache backend is not RedisBackend. Pattern clearing only supported for Redis.")

    # Construct pattern based on prefix and namespace
    pattern = f"{prefix}:{namespace}*"

    logger.debug(f"Clearing cache with pattern: {pattern}")

    # Scan and delete all keys matching the pattern
    async for key in cache_backend.redis.scan_iter(match=pattern):  # type: ignore
        logger.debug(f"Deleting cache key: {key}")
        await cache_backend.redis.delete(key)  # type: ignore


async def clear_cache_by_pk(pk: str, namespace: str = "") -> None:
    """
    Clear the cache for a specific cache by its primary key (pk).
    """
    prefix = FastAPICache.get_prefix()
    cache_backend = FastAPICache.get_backend()

    if namespace == "":
        cache_key = f"{prefix}:{pk}"
    else:
        cache_key = f"{prefix}:{namespace}:{pk}"

    logger.debug(f"Clearing cache for key: {cache_key}")

    # https://github.com/long2ice/fastapi-cache/blob/main/fastapi_cache/backends/redis.py
    await cache_backend.clear(key=cache_key)


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
