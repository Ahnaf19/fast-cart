# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from inventory.app.db.redis import get_redis_om_client
from inventory.app.routes.route import router

# Create an instance of the FastAPI application
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])


@app.on_event("startup")
async def startup_event() -> None:
    """
    Event handler for application startup.
    """
    app.state.redis = get_redis_om_client()
    logger.info("Application is starting up...")
    logger.debug("Redis connection initialized and stored in app.state")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Event handler for application shutdown.
    """
    app.state.redis.close()
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
