# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from inventory.app.routes.route import router

# from loguru import logger

# load_dotenv()


# from inventory.app.db.redis import redis_db

# logger.debug(f"Redis Connection Params in FastAPI: {redis_db.connection_pool.connection_kwargs}")

# Create an instance of the FastAPI application
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])

# Include routers for guest and room endpoints
app.include_router(router)


def main() -> None:
    """
    Entry point for the application when run explicitly.
    """
    print("main.py running explicitly")


if __name__ == "__main__":
    main()
