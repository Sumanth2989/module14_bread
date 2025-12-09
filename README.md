# Module 11 – SQLAlchemy Model, Pydantic Schemas, Factory Pattern & CI/CD

This module implements the Calculation feature using SQLAlchemy, Pydantic, a Factory design pattern, and a full CI/CD pipeline with GitHub Actions and Docker Hub. It includes unit tests, integration tests with PostgreSQL, Alembic migrations, and automated Docker image builds and pushes.

## Features Implemented

### SQLAlchemy Calculation Model
- Fields: id, a, b, type, result
- Enum-based operation types: add, sub, multiply, divide
- Alembic migrations fully functional

### Pydantic Schemas
- CalculationCreate for validating inputs
- CalculationRead for returning responses
- Validation prevents division by zero and invalid types

### Factory Pattern
Implements strategies:
- AddStrategy
- SubStrategy
- MultiplyStrategy
- DivideStrategy

This ensures extensibility for future operations.

### Testing
- Unit tests: Factory logic + Pydantic rules
- Integration tests: Database persistence using SQLAlchemy + Alembic
- All tests pass locally and in CI

## Run Tests Locally

pip install -r requirements.txt  
pytest -q

## Database Migrations

alembic upgrade head

## Build & Run Docker Image Locally

docker build -t module11-sql .  
docker run -p 8000:8000 module11-sql

## CI/CD Pipeline (GitHub Actions)

Every push to main:
1. Installs dependencies
2. Runs tests
3. Builds Docker image
4. Pushes image to Docker Hub

Workflow file: .github/workflows/ci.yml

## Docker Hub Repository Link

https://hub.docker.com/r/sumanthchand23/module11-sql

## Project Structure

app/
 ├── models/
 │    └── calculation.py
 ├── schemas/
 │    └── calculation.py
 ├── services/
 │    ├── calculation_factory.py
 │    └── calculation_service.py
alembic/
 ├── versions/
tests/
 ├── unit/
 ├── integration/
.github/
 └── workflows/
     └── ci.yml

# Module 12 
# Module 12 – FastAPI Calculator (Users + Calculations + CI/CD + Docker)

This project is an upgraded version of the Module 11 FastAPI calculator.  
In Module 12, we add **user authentication**, **CRUD operations for calculations**, full **integration tests**, and **CI/CD with Docker Hub** using GitHub Actions.

---

## Features

### **User Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register a new user with email + password |
| POST | `/users/login` | Log in and verify password |

### **Calculation Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/calculations/` | Browse all calculations |
| POST | `/calculations/` | Add a new calculation |
| GET | `/calculations/{id}` | Read a single calculation |
| PUT | `/calculations/{id}` | Edit a calculation |
| DELETE | `/calculations/{id}` | Delete a calculation |

### **Other Features**
- Password hashing using **Passlib (bcrypt)**  
- SQLAlchemy ORM models  
- Pydantic schemas  
- PostgreSQL support  
- Fully automated GitHub Actions pipeline  
- Docker image build + push to Docker Hub  
- Integration tests for users + calculations

---

## Project Structure

```
module12_calci/
│── app/
│   ├── auth.py
│   ├── database.py
│   ├── models/
│   │   └── calculation.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── calculation.py
│   └── routers/
│       ├── users.py
│       └── calculations.py
│
│── tests/
│   └── integration/
│       ├── test_users.py
│       └── test_calculations.py
│
│── Dockerfile
│── requirements.txt
│── main.py
│── README.md
│── .github/workflows/ci.yml
```

---

## Running tests locally

Make sure dependencies are installed:

```sh
pip install -r requirements.txt
```

Run all tests:

```sh
pytest -q
```

You should see all tests passing:

```
............. [100%]
```

---

## Running with Docker

### Build the image:

```sh
docker build -t module12-calci .
```

### Run the container:

```sh
docker run -p 8000:8000 module12-calci
```

Open your browser:

```
http://127.0.0.1:8000/docs
```

---

## GitHub Actions + Docker Hub Deployment

This project includes a CI/CD workflow that:

1. Installs dependencies  
2. Spins up a PostgreSQL container  
3. Runs integration tests  
4. Builds a Docker image  
5. Pushes the image to Docker Hub  

### **.github/workflows/ci.yml**

```yaml
name: CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  test-build-deploy:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U test_user -d test_db"
          --health-interval=5s
          --health-timeout=5s
          --health-retries=5

    env:
      DATABASE_URL: postgresql+psycopg2://test_user:test_password@localhost:5432/test_db
      DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
      IMAGE_NAME: ${{ secrets.DOCKERHUB_USERNAME }}/module12-calci

    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest -q

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ env.DOCKERHUB_USERNAME }}
          password: ${{ env.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: |
            ${{ env.IMAGE_NAME }}:latest
            ${{ env.IMAGE_NAME }}:${{ github.sha }}
```

---

## Endpoints (Sample Requests)

### Register
```json
{
  "email": "newuser@example.com",
  "password": "secret123"
}
```

### Login
```json
{
  "email": "newuser@example.com",
  "password": "secret123"
}
```

### Add Calculation
```json
{
  "a": 10,
  "b": 5,
  "type": "add"
}
```

---

## 🎯 Summary

You now have a fully functional:

- FastAPI application  
- User auth system  
- Calculation CRUD features  
- Full automated CI/CD pipeline  
- Dockerized deployment  
- Integration-tested backend  

# Module 13 - Assignment-JWT Login/Registration with Client-Side Validation & Playwright E2E
# Module 13 Documentation

## Overview
Module 13 focuses on building full-stack functionality around user authentication and calculation management. It includes implementing REST API endpoints, configuring database interactions, writing integration tests, and preparing the project for CI/CD deployment.

---

## Features Implemented

### 1. User Registration (POST /users/register)
- Accepts `UserCreate` schema input.
- Hashes the user password before saving it.
- Stores user details in the database.
- Returns the created user's public information.

### 2. User Login (POST /users/login)
- Verifies hashed passwords using a secure comparison algorithm.
- Validates credentials against stored user data.
- Returns a success message or token if implementing authentication.

---

## Calculation Endpoints (BREAD)

### Browse (GET /calculations)
- Returns a list of all saved calculations.

### Read (GET /calculations/{id})
- Fetches a single calculation by ID.
- Returns 404 if not found.

### Edit (PUT/PATCH /calculations/{id})
- Updates an existing calculation’s details.
- Validates input using `CalculationCreate` or relevant schema.

### Add (POST /calculations)
- Creates a new calculation.
- Validates input with `CalculationCreate` schema.

### Delete (DELETE /calculations/{id})
- Removes a calculation entry.
- Returns success or not found.

---

## Integration Tests

### Test Coverage Includes:
- Successful and failing user registration.
- Login with correct and incorrect credentials.
- CRUD operations on calculations.
- Database state validation after operations.

### Tools Used:
- pytest
- httpx test client
- FastAPI's dependency overrides for test DB

---

## OpenAPI Verification
- All endpoints were tested using `/docs` and `/redoc`.
- Input and output schemas validated.
- Ensured correct status codes and response formats.

---

## GitHub Actions + Deployment
- Automated tests run in CI.
- Postgres service is spun up dynamically.
- Successful builds push image to Docker Hub.


# Module14 Bread Dockerized Application

This repository contains a Python-based application packaged and deployed using Docker. The application uses FastAPI and SQLite. This document provides instructions for building, running, and pushing the Docker image.

## Prerequisites

- Docker installed on your system: [Docker Installation Guide](https://docs.docker.com/get-docker/)
- Python 3.11 (for local development if needed)
- Docker Hub account
- `app/`: Contains the main application code.
- `test.db`: Initial SQLite database file.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Instructions to build the Docker image.

## Usage Flow

Register: Navigate to /register to create a new user account.

Login: Log in with your new credentials at /login.

BREAD Operations: You will be redirected to /calculations, where you can perform all BREAD operations:

Browse/List: View all past calculations.

Add: Click the "Add New Calculation" link.

View: You can search for particular calculations based on their id.

Edit: Click the "Edit" link to modify the operands.

Delete: Click the "Delete" button.

 Executing Tests Locally

To prove the application's functionality and security, run the automated E2E tests.

## Dockerfile Overview

1. **Builder Stage**
   - Uses `python:3.11-slim` as the base image.
   - Installs build dependencies like `gcc`.
   - Copies `requirements.txt` and installs Python packages.

2. **Runtime Stage**
   - Uses `python:3.11-slim` as a smaller runtime image.
   - Copies Python packages from the builder stage.
   - Copies application code and `test.db`.
   - Exposes port `8000` for FastAPI.
   - Runs the application with Uvicorn.

## Building the Docker Image

```bash
docker build -t module14_bread .
Running the Docker Container Locally
docker run -d -p 8000:8000 module14_bread
Visit http://localhost:8000 to access the application.

