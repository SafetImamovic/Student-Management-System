# Roadmap Development Logs

## Roadmap Overview

### Project Description

Title: Student Management System Internship Project

Objective: To provide the intern with practical experience in building and managing APIs using
FastAPI, PostgreSQL, Alembic, and Pydantic.

The intern will learn how to create models, handle
CRUD operations, validate data, and understand the integration of a relational database with a web
API.

The project will be focused on creating a simple Student Management System.

Project Theme: The Student Management System will have two main tables:
- students
- courses


The students table will store information about students, such as their name, age, and email. The
courses table will store information about courses, such as the course name and description. The
project will involve creating APIs to manage the students and courses, including operations to
create, read, update, and delete records.
Goals:

1. Deepen understanding of Python fundamentals.
2. Gain practical experience with FastAPI.
3. Learn how to use PostgreSQL for database management.
4. Understand database migrations using Alembic.
5. Implement CRUD operations and API endpoints.
6. Validate data using Pydantic models.
   
### Week 1: Introduction & Setup

Description:

Set up the development environment. Introduction to FastAPI, PostgreSQL, Alembic, and Pydantic.

Basic Python review.

Prerequisites:

Basic knowledge of Python (variables, data types, loops, functions). Installations: Python, FastAPI,
PostgreSQL, Alembic, Pydantic.

Resources:

- FastAPI Documentation: [](https://fastapi.tiangolo.com/)
- PostgreSQL Installation Guide: [](https://www.postgresql.org/download/)
- Alembic Documentation: [](https://alembic.sqlalchemy.org/en/latest/)
- Pydantic Documentation: [](https://pydantic-docs.helpmanual.io/)
- Basic Python Tutorial: [](https://docs.python.org/3/tutorial/)

Goal:
Have a fully set up development environment. Basic understanding of FastAPI, PostgreSQL,
Alembic, and Pydantic. Create a simple 'Hello World' API using FastAPI.

### Week 2: Database Integration & Models

Description:

Introduction to SQLAlchemy for ORM. Creating PostgreSQL database and tables. Setting up
database models in FastAPI. Using Pydantic for data validation.

Prerequisites:

Basic understanding of databases and SQL. Completed Week 1 tasks.
Resources:

- SQLAlchemy Documentation: [https://docs.sqlalchemy.org/en/14/](https://docs.sqlalchemy.org/en/14/)
- FastAPI with SQLAlchemy Tutorial: [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- Pydantic with FastAPI Tutorial: [https://fastapi.tiangolo.com/tutorial/body/](https://fastapi.tiangolo.com/tutorial/body/)
- PostgreSQL Tutorial: [https://www.postgresqltutorial.com/](https://www.postgresqltutorial.com/)

Goal:

Create two tables in PostgreSQL: students and courses. Define SQLAlchemy models for these
tables in FastAPI. Define Pydantic models for data validation. Connect FastAPI to PostgreSQL.

### Week 3: CRUD Operations

Description:

Implement CRUD operations (Create, Read, Update, Delete). Develop API endpoints for CRUD
operations. Validate data using Pydantic models.

Prerequisites:

Completed Week 2 tasks.

Resources:
- FastAPI CRUD Tutorial:
[https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-tables](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-tables)
- Postman Documentation for API Testing:
[https://learning.postman.com/docs/getting-started/introduction/](https://learning.postman.com/docs/getting-started/introduction/)
- Pydantic Validation: [https://pydantic-docs.helpmanual.io/usage/validators/](https://pydantic-docs.helpmanual.io/usage/validators/)

Goal:

Implement and test CRUD operations for the students and courses models. Ensure proper
functioning of API endpoints using tools like Postman. Validate request and response data using
Pydantic models.

### Week 4: Database Migrations & Final Project

Description:

Introduction to Alembic for database migrations. Perform database migrations. Finalize the project
and prepare for presentation.

Prerequisites:

Completed Week 3 tasks.

Resources:
- Alembic Tutorial: [https://alembic.sqlalchemy.org/en/latest/tutorial.html](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- FastAPI Deployment: [https://fastapi.tiangolo.com/deployment/](https://fastapi.tiangolo.com/deployment/)

Goal:

Perform at least one database migration using Alembic. Finalize and document the project. Prepare
a presentation/demo of the project.