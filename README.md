<a href="https://safetimamovic.github.io/Student-Management-System/starter-topic.html"><img src="https://img.shields.io/badge/Project%20Documentation-gray" alt="Project Documentation"></a>

# Student Management System

## Quick Setup

To run the application, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SafetImamovic/Student-Management-System
   ```
   
2. Create the appropriate `.env` and `.env.docker` files as explained in [Environment Variables](#environment-variables).


3. **Start the Docker containers:**

   ```bash
   ./scripts/start
   ```

4. **Verify that the containers are running:**

   ```bash
   docker ps
   ```

5. **Access the application in your browser:**

   - Backend: [http://localhost:8000/](http://localhost:8000/)
   - Frontend: [http://localhost:80/](http://localhost:80/)


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


### Environment Variables

These are examples of the environment variables required to run the application locally.
You should replace `password`, `localhost`, and other values with the appropriate details for your setup.

### Example `.env` File

Create a file named `.env` in the root of the project with the following content:

```env
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432" # by default
POSTGRES_USER="postgres" # by default
POSTGRES_PASSWORD=password
POSTGRES_NAME="student_management_system_db" # by default
```

### Example `.env.docker` File

Create a file named `.env.docker` in the root of the project with the following content:

```env
POSTGRES_HOST=host
POSTGRES_PORT="5432" # by default
POSTGRES_USER="postgres" # by default
POSTGRES_PASSWORD=password
POSTGRES_NAME="student_management_system_db" # by default
```

Main difference between these 2 .env files is the `POSTGRES_HOST`.
- In `.env` the host should be 'localhost'.
- In `.env.docker` the host should be the container name.


### `.env` vs. `.env.docker` for SQLAlchemy URL

> The default database name is `student_management_system_db`.

> If you're running the Docker containers using `./scripts/start.sh`, this will run `docker compose up --build` with `student-management-system-db-server`
> being the default name for the Database container.
>
> With this in mind:

- **`.env` File:**
  - **Path:** The `.env` file is configured for local development where the database is accessed directly from your local machine.
  - **SQLAlchemy URL:**
    ```plaintext
    SQL_ALCHEMY_URL=postgresql://postgres:password@localhost:5432/student_management_system_db
    ```
    - **Explanation:** The database is hosted on the local machine (`localhost`), and the application connects to it directly.

- **`.env.docker` File:**
  - **Path:** The `.env.docker` file is configured for a Docker environment where the database is running within a Docker container.
  - **SQLAlchemy URL:** docker ps
  - 
    ```plaintext
    SQL_ALCHEMY_URL=postgresql://postgres:password@student-management-system-db-server:5432/student_management_system_db
    ```
    - **Explanation:** In a Docker setup, the database container is named `postgres`, so the application connects to it using the container name as the host.



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