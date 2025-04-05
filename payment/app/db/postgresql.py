import importlib
import os
import pkgutil
from typing import Annotated, AsyncGenerator

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# from payment.app.models.models import Order
# * used dynamic import instead
from payment.app.models import models  # noqa: F401

# from typing import Annotated

# from dotenv import load_dotenv
# from fastapi import Depends
# from sqlmodel import Session, SQLModel, create_engine


load_dotenv()

POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# weirdly .env stores/reads int as str
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")

# url --> postgresql://{username}:{password}@{host}:{port}/{database}

URL_DATABASE = (
    f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
)

# engine = create_engine(URL_DATABASE, echo=True)

URL_ASYNC_DATABASE = (
    f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
)

async_engine = create_async_engine(URL_ASYNC_DATABASE, echo=True)


def import_models():
    """
    Dynamically imports all modules in the 'models' package.

    This function iterates over all modules in the 'models' package directory
    and imports them using their module names. It assumes that the 'models'
    package is located under 'payment.app.models'.

    Note:
        Ensure that the 'models' package is properly structured and accessible
        in the specified path.

    Raises:
        ImportError: If a module cannot be imported.
    """
    for _, module_name, _ in pkgutil.iter_modules(["payment/app/models"]):  # Path to models directory
        importlib.import_module(f"payment.app.models.{module_name}")


async def create_db_and_tables() -> None:
    """
    Creates the database and all associated tables if they do not already exist.

    This function dynamically imports all models using the `import_models` function
    and then utilizes SQLModel's metadata to create the necessary database schema
    by binding it to the specified engine.

    Note:
        Ensure that the `engine` is properly configured and that all models
        are correctly defined and imported before calling this function.
    """
    import_models()  # Dynamically import all models
    # SQLModel.metadata.create_all(bind=engine)
    async with async_engine.begin() as conn:
        # Create the database if it doesn't exist
        await conn.run_sync(SQLModel.metadata.create_all)


def get_session():
    """
    Provides a generator function to yield a database session.

    This function creates a new session using the provided database engine
    and yields it for interacting with the database. The session is automatically
    closed when the context is exited.

    Yields:
        Session: A SQLAlchemy session object for database operations.
    """
    # with Session(engine) as session:
    #     yield session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


# SessionDep = Annotated[Session, Depends(get_session)]
SessionDep = Annotated[AsyncSession, Depends(get_db)]
