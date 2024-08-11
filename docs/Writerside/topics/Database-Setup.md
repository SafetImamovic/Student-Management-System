# 4. Database ORM Setup

## Test Database

Before setting up the ORM a test database is created called `test_db`.

Because of predefined quick start guide, we can run the following command to start 
the FastAPI server as well as the PostgreSQL database:
```Bash
./scripts/start
```
To initialize a PSQL Client container to interact with the database the following command is run:
```Bash
./scripts/start-psql-client
```

After being prompted for the password, the following command is run to list the databases:
```Bash
\l
```

<procedure title="Console Output">

```Bash
postgres=# \l
                                                      List of databases
   Name    |  Owner   | Encoding | Locale Provider |  Collate   |   Ctype    | ICU Locale | ICU Rules |   Access privileges
-----------+----------+----------+-----------------+------------+------------+------------+-----------+-----------------------
 postgres  | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |
 template0 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres          +
           |          |          |                 |            |            |            |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres          +
           |          |          |                 |            |            |            |           | postgres=CTc/postgres
```
These are the default databases that come with the PostgreSQL image.

</procedure>

To create a new database the following command is run:
```Bash
create database test_db;
```

<procedure title="Console Output">

```Bash
postgres=# create database test_db;
CREATE DATABASE
postgres=# \l
                                                      List of databases
   Name    |  Owner   | Encoding | Locale Provider |  Collate   |   Ctype    | ICU Locale | ICU Rules |   Access privileges
-----------+----------+----------+-----------------+------------+------------+------------+-----------+-----------------------
 postgres  | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |
 template0 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres          +
           |          |          |                 |            |            |            |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres          +
           |          |          |                 |            |            |            |           | postgres=CTc/postgres
 test_db   | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |
(4 rows)
```
</procedure>

To ensure that the database has no relations, the following commands are run:
```Bash
postgres=# \c test_db
You are now connected to database "test_db" as user "postgres".
test_db=# \d
Did not find any relations.
```

## Package Structure

Two new python files are created in the `app/` directory:
```text
student-management-system (root)
└── app/
    ├── __init__.py
    ├── database.py
    ├── main.py
    └── models.py
    ...
```



The `database.py` file is created to handle the database connection and session creation.

The `models.py` file is created to define the SQLAlchemy models.

The `__init__.py` file is created to make the `app` directory a package.

## Database Connection
`database.py`:
```Python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
```

Import Statements:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
```

- **`create_engine`**: This function is used to create a new SQLAlchemy engine instance, which is the starting point for any SQLAlchemy application.
- **`declarative_base`**: This function is used to create a base class for declarative class definitions. All model classes will inherit from this base class.
- **`sessionmaker`**: This function is a factory for creating new `Session` objects. A `Session` is used to interact with the database.

### Database URL

```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/test_db"
```

- **`SQLALCHEMY_DATABASE_URL`**: This is the connection string for the PostgreSQL database. It follows the format:
  ```
  postgresql://username:password@host:port/database
  ```

### Creating the Engine

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

- **`engine`**: The `engine` object is created using the connection string. This object manages the connection pool and database connections. It's the entry point to the database in SQLAlchemy.

### Creating a Session Factory

```python
SessionLocal = sessionmaker(bind=engine)
```

- **`SessionLocal`**: This is a session factory bound to the `engine`. The `sessionmaker` function returns a class that can be used to create new `Session` objects. When a session is created from this factory, it will use the `engine` to connect to the database.

### Creating a Declarative Base

```python
Base = declarative_base()
```

- **`Base`**: This is the base class for all ORM (Object-Relational Mapping) models. When you define a model class, it will inherit from `Base`. This base class maintains a catalog of classes and tables relative to that base.

### How These Components Work Together

1. **Engine**:
    - The `engine` is the core interface to the database, providing connectivity and the ability to execute raw SQL or ORM queries.

2. **Session**:
    - The `SessionLocal` factory creates session objects. These sessions are used to interact with the database, handling transactions, and queries.
    - We typically use a session to add, update, delete, or query rows in the database.

3. **Base**:
    - The `Base` class is used to define ORM models. Each model represents a table in the database, and each attribute of the model represents a column in the table.
    - When a model class is defined inheriting from `Base`, SQLAlchemy knows how to map it to a table in the database.

### Testing the Database Connection

`models.py`:
```Python
import datetime
from sqlalchemy import Column, Integer, DateTime
from .database import Base


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

```

Import Statements:

```python
import datetime
from sqlalchemy import Column, Integer, DateTime
from .database import Base
```

1. **`import datetime`**:
    - This imports Python's built-in `datetime` module, which provides classes for manipulating dates and times.

2. **`from sqlalchemy import Column, Integer, DateTime`**:
    - **`Column`**: This is a SQLAlchemy class used to define a column in a database table.
    - **`Integer`**: This specifies that the column will store integer values.
    - **`DateTime`**: This specifies that the column will store date and time values.

3. **`from .database import Base`**:
    - This imports the `Base` class from a local module named `database`. The `Base` class is the declarative base used to define the ORM models. It's typically created with `declarative_base()` in the main configuration file.

### Defining the `Test` Model

```python
class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
```

1. **`class Test(Base):`**:
    - This defines a new ORM model class named `Test` which inherits from `Base`. By inheriting from `Base`, the `Test` class is recognized by SQLAlchemy as a mapped class.

2. **`__tablename__ = 'test'`**:
    - This class attribute specifies the name of the database table associated with this model. In this case, the table will be named `test`.

3. **Defining Columns**:
    - **`id = Column(Integer, primary_key=True)`**:
        - This defines a column named `id` in the `test` table.
        - The column's data type is `Integer`.
        - The column is marked as the primary key (`primary_key=True`). This means that the `id` column will uniquely identify each row in the table.

    - **`created_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))`**:
        - This defines a column named `created_date` in the `test` table.
        - The column's data type is `DateTime`, which will store date and time values.
        - The column has a default value specified by `default=datetime.datetime.now(datetime.timezone.utc)`. This means that if no value is provided for `created_date` when a new row is inserted, the current date and time (in UTC) will be used as the default value.

### How It Works Together

1. **Model Definition**:
    - The `Test` class defines a table schema with two columns: `id` and `created_date`. The `id` column is an integer primary key, and `created_date` is a datetime column with a default value.

2. **Table Mapping**:
    - By inheriting from `Base` and defining `__tablename__`, SQLAlchemy knows to map instances of the `Test` class to rows in the `test` table.

3. **Column Attributes**:
    - Each attribute of the `Test` class corresponds to a column in the `test` table. The data types and constraints (like primary key and default values) are specified using SQLAlchemy's `Column` class.

## Summary

In this section we have:

- Created a test database called `test_db`.
- Defined the database connection and session creation in `database.py`.
- Defined the `Test` model in `models.py`.