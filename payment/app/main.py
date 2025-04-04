from contextlib import asynccontextmanager

from fastapi import FastAPI

from payment.app.db.postgresql import create_db_and_tables
from payment.app.routes.CRUD_route import router as crud_router
from payment.app.routes.route import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event to initialize the database at startup.
    """
    await create_db_and_tables()  # Ensures tables are created on startup
    yield  # No need to keep anything persistent
    # No explicit DB close required because we use per-request sessions


app = FastAPI(lifespan=lifespan)

app.include_router(router)  # * main order routes
app.include_router(crud_router)  # * reference CRUD routes


def main() -> None:
    """
    Entry point for the application when run explicitly.
    """
    print("main.py running explicitly")


if __name__ == "__main__":
    main()
