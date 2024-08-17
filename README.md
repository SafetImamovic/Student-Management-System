<a href="https://safetimamovic.github.io/Student-Management-System/starter-topic.html"><img src="https://img.shields.io/badge/Project%20Documentation-gray" alt="Project Documentation"></a>

# Student Management System

## Quick Setup

This project uses Docker to run FastAPI and PostgreSQL in separate containers.

It also runs a vanilla html, css and js frontend container.

### FastAPI & PostgreSQL

To run the FastAPI, PostgreSQL & Frontend containers run the following command in the project root:

```Bash
./scripts/start
```

This script will create a shared network, build the FastAPI and Frontend image, start the FastAPI, PostgreSQL & Frontend containers, and output the container logs.

After successful builds, running `docker ps` should show the active containers.

Then visiting `http://localhost:8000/` in a browser will result with the html body of:

```Bash
{"Hello": "World"}
```

And visiting `http://localhost:80/` in a browser will result in the Frontend Website:

<img src="docs\Writerside\images\frontend.png">

### PostgreSQL Client

To run a PSQL client as a container run:

```Bash
./scripts/start-psql-client
```

This script starts a new container based on the postgres docker image.
This container isn't specified in the docker compose file rather this 
should be run if you don't want to download and install the postgres 
driver locally.

It starts the client and connects to the network on which the database is
already on. If the database container isn't active the client will throw 
errors.

### Stopping & Clean Up

To stop the containers run:

```Bash
docker-compose down
```

or run:

```Bash
./scripts/clean-up
```

### Additional Options

For some more options when it comes to handling the client container and network.

> You can also run:
> ```Bash
> ./scripts/{script name} --help
> ```
> To see how they work.

[_More details on setting up Docker, Dockerfile and Docker Compose can be found here_](https://safetimamovic.github.io/Student-Management-System/docker.html)

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