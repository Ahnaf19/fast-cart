from fastapi import FastAPI

from payment.app.routes.route import router

# Create an instance of the FastAPI application
app = FastAPI()

# Include routers for guest and room endpoints
app.include_router(router)


def main() -> None:
    """
    Entry point for the application when run explicitly.
    """
    print("main.py running explicitly")


if __name__ == "__main__":
    main()
