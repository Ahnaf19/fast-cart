from typing import Optional

from fastapi_cache import FastAPICache
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response


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
