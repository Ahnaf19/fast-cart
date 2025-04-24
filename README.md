# fast-cart

**fast-cart** is a microservices-based e-commerce backend designed for high performance and scalability.

## Project Overview

The project is designed to consist of two microservices:

1. **Inventory Service**:
   This service manages product inventory, including stock levels, product details, and updates. It interacts with a redis database for storage, using redis for caching as well.

2. **Payment Service**:
   This service handles payment processing, order validation, and transaction management, stored in postgresql. It also interacts with the Inventory Service to validate stock availability before processing payments. It also uses redis for caching as well.

3. **Inventory Frontend**
   This service provides a user interface for managing inventory. It allows users to:

   - View product details and stock levels.
   - Add, update, or delete products.
   - Monitor inventory changes in real-time.

   The frontend is built using **React** for a responsive and dynamic user experience. It communicates with the Inventory Service via RESTful APIs to fetch and update data.

   ### Setup Instructions

   1. Navigate to the `inventory-frontend` directory.
   2. Install dependencies:

   ```sh
   npm install
   ```

   3. Start the development server:

   ```sh
   npm run dev
   ```

   4. Access the application at `http://localhost:3000`.

4. **Payment Frontend**

   > in progress

5. **Event Driven Architecture**

   Event-driven architecture enables seamless communication between the Payment and Inventory services using Redis Streams. When a payment is processed, the Payment Service publishes an event to a Redis stream. The Inventory Service subscribes to this stream, listens for payment events, and updates stock levels accordingly. This decoupled approach ensures scalability, real-time updates, and fault tolerance in the system. Also makes it easier to catch rare edge cases.

### Key Technologies

- **FastAPI**: For building high-performance APIs with Python.
- **Redis**: For caching and message brokering between microservices.
- **Redis Stream**: Used for event driven architecture.
- **SQL Database**: For persistent storage of inventory and payment data.
- **Docker**: For containerizing the microservices for easy deployment and scalability.
- **GitHub Actions**: For CI/CD pipelines to ensure code quality and automated testing.
- **Pre-commit Hooks**: For enforcing code formatting and linting standards.

### Microservice Interaction

The two microservices will communicate with each other using RESTful APIs with `FastAPI`. `Redis` will be used as a message broker for asynchronous tasks, such as updating inventory after a successful payment: part of event driven architecture.

### Future Enhancements

[x] Use SQL for persistant storage and redis for caching.
[ ] Add authentication and authorization mechanisms.
[x] Implement monitoring and logging for better observability.
[ ] Explore deployment options such as Kubernetes for scaling the microservices.

This project aims to serve as a robust starting point for building scalable and maintainable microservices with Python.

> [!NOTE]
> [Check Milestones](#milestones) below to track project progress.

---

> Being developed on: python 3.10.16

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Pydantic](https://img.shields.io/badge/pydantic-4A91A2?style=for-the-badge&logo=python&logoColor=white) ![Pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white) ![Uvicorn](https://img.shields.io/badge/uvicorn-111111?style=for-the-badge&logo=uvicorn&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white) ![Loguru](https://img.shields.io/badge/loguru-FF9C00?style=for-the-badge&logo=python&logoColor=white)

![Black](https://img.shields.io/badge/black-000000?style=for-the-badge&logo=python&logoColor=white) ![isort](https://img.shields.io/badge/isort-4B8BBE?style=for-the-badge&logo=python&logoColor=white) ![flake8](https://img.shields.io/badge/flake8-306998?style=for-the-badge&logo=python&logoColor=white) ![mypy](https://img.shields.io/badge/mypy-2A6DB2?style=for-the-badge&logo=python&logoColor=white) ![bandit](https://img.shields.io/badge/bandit-CD5C5C?style=for-the-badge&logo=python&logoColor=white) ![Pre-commit](https://img.shields.io/badge/pre--commit-FAAF3A?style=for-the-badge&logo=pre-commit&logoColor=white) ![CodeQL](https://img.shields.io/badge/codeql-006F99?style=for-the-badge&logo=github-actions&logoColor=white)

![GitHub Actions](https://img.shields.io/badge/github%20actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

---

## Docker Build & Run

To build and run the application using Docker, follow these steps:

---

### Prerequisites

Ensure you have Docker installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).

#### Build Docker Image

> [!IMPORTANT]
> `Docker Daemon` or `Docker Desktop` must be running while building Docker Image.

Navigate to the root directory of the repo where the `Dockerfile` is located and run the following command to build the Docker image:

```sh
docker build -t fastcart:latest .
```

#### Run Docker Container

After building the Docker image, you can run it using the following command:

```sh
docker run -dp 8000:8000 <fastcart>:latest
```

or give the container a name:

```sh
docker run -dp 8000:8000 --name <fastcart>-latest <fastcart>:latest
```

This will start the application in a Docker container. The application can be accessed at `http://localhost:8000` e.g. `127.0.0.1:8000`

> [!NOTE]
> `-dp` (`-d` & `-p`) tag runs the container in detached mode (in the background, terminal is available to use right away) and container port `8000` is mapped to local port `8000`.

#### Stopping the Container

To stop the running container, first find the container ID using:

```sh
docker ps
```

Then stop the container using:

```sh
docker stop <container_id>
```

---

## Run locally with Uvicorn

> this part is yet to be updated with repo structure

- [optional but recommended] create a venv and activate it
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- start Uvicorn server:
  ```sh
  uvicorn app.main:app --reload
  ```
- `ctrl+c` to break the server.

---

## Milestones

- [x] develop inventory api 🤖
- [x] develop payment api ✨
- [x] Interact between the microservices 🌐
- [ ] unit testing 🧪
- [ ] write comprehensive readme 📖
- [ ] write readme-dev 📖
- [ ] dockerize the repo 🐳
- [x] Code Auto-formatting & Linting with Pre-commit (check-yaml, end-of-file-fixer, trailing-whitespace, black, isort, mypy, flake8, bandit) 🎨
- [x] add GitHub Action for format checks ✅
- [ ] Study deploy requirement and deploy! 🚀

---

## Collaborate & Contribute

Bug reports, issues, forks and pull requests are always welcome!

---

## License

This project is available as open source under the MIT License. See the [LICENSE](./LICENSE) file for details.
