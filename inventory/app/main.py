from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger

from inventory.app.db.redis import get_redis_cache_client, get_redis_om_client
from inventory.app.models.models import Product
from inventory.app.routes.route import router

# Create an instance of the FastAPI application
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])

# Initialize a variable to store the redis_cache instance
redis_cache = None


@app.on_event("startup")
async def startup_event() -> None:
    """
    Event handler for application startup.
    """
    # Initialize Redis OM client for data operations
    app.state.redis = get_redis_om_client()

    # Initialize Redis client for caching
    global redis_cache
    redis_cache = get_redis_cache_client()
    FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")

    # Set model Redis database and prefix in meta
    Product.set_meta_attr(app.state.redis, global_key_prefix="fastcart", model_key_prefix="inventory")

    logger.info("Application is starting up...")
    logger.debug("Redis connection initialized and stored in app.state")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Event handler for application shutdown.
    """
    app.state.redis.close()
    if redis_cache:
        await redis_cache.close()

    logger.debug("Redis connection closed during app shutdown")
    logger.info("Application is shutting down...")


# Include routers for guest and room endpoints
app.include_router(router)


def main() -> None:
    """
    Entry point for the application when run explicitly.
    """
    print("main.py running explicitly")


if __name__ == "__main__":
    main()
