<a href="https://github.com/SafetImamovic/Student-Management-System/blob/main/README.md"><img src="https://img.shields.io/badge/Lang-EN-red" alt=""></a> <a href="https://github.com/SafetImamovic/Student-Management-System/blob/main/README.bs.md"><img src="https://img.shields.io/badge/Lang-BS-blue" alt="Project Documentation"></a> <a href="https://safetimamovic.github.io/Student-Management-System/starter-topic.html"><img src="https://img.shields.io/badge/Project%20Documentation-gray" alt="Project Documentation"></a>

# Student Management System

## Quick Setup

This project uses Docker to run FastAPI and PostgreSQL in separate containers.

To run the FastAPI and PostgreSQL containers run the following command in the project root:

```Bash
./start
```

This script will create a shared network, build the FastAPI image, start the FastAPI and PostgreSQL containers, and output the container logs.

After successful builds, running `docker ps` should show the active containers.

To stop the containers run:

```Bash
docker-compose down
```

> You can also run:
> ```Bash
> ./start --help
> ```

Then visiting `http://localhost:8000/` or `http://127.0.0.1:8000/` in a browser will result with the html body of:

```Bash
{"Hello": "World"}
```

[_More details on setting up Docker, Dockerfile and Docker Compose can be found here_](https://safetimamovic.github.io/Student-Management-System/docker.html)

> Volumes aren't integrated yet, so live updates don't work

## Objective

This project is designed to provide practical experience in building and managing APIs using:
- **FastAPI**
- **PostgreSQL**
- **Alembic**
- **Pydantic**

The main focus will be on developing a simple Student Management System: creating models, handling CRUD operations, validating data, and integrating a relational database with a web API.

## Project Timeline

This project spans across 4 weeks:

### Week 1: Introduction & Setup

Set up the development environment and get introduced to FastAPI, PostgreSQL, Alembic, and Pydantic. Review basic Python concepts.

### Week 2: Database Integration & Models

Learn about SQLAlchemy for ORM, create PostgreSQL databases and tables, set up database models in FastAPI, and use Pydantic for data validation.

### Week 3: CRUD Operations

Implement CRUD operations and develop API endpoints for these operations. Validate data using Pydantic models.

### Week 4: Database Migrations & Final Project

Get introduced to Alembic for database migrations, perform database migrations, and finalize the project for presentation.

> _The project timeline is subject to change_