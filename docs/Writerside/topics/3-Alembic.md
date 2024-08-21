# 3. Alembic & SQLAlchemy

## Description

[Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.

Alembic works with SQLAlchemy by managing and automating database schema migrations based on changes made to the SQLAlchemy models.

## Installation

Alembic is not a part of the standard FastAPI installation, it can be installed running:

```Bash
pip install alembic
```

Then the `requirements.txt` is updated:

```Bash
pip freeze > requirements.txt
```

Alembic’s install process will ensure that SQLAlchemy is installed, in addition to other dependencies, as stated on the official website.

The resulting file structure looks like this after the _Migration Environment_ is installed:

```text
student-management-system (root)
├── ...
├── requirements.txt
├── alembic.ini         # +
├── alembic/            # +
│   ├── env.py          # +
│   ├── README          # +
│   ├── script.py.mako  # +
│   └── versions/       # +
└── ...
```

## Migration Environment Structure

File created at project root:
- `alembic.ini` - This is a file that the alembic script looks for when invoked.

Files and dirs within the `alembic` dir:
- `env.py` - This is a Python script that is run whenever the alembic migration tool is invoked.
- `README.md` - Included with the various environment templates, should have something informative.
- `script.py.mako` - This is a Mako template file which is used to generate new migration scripts. Whatever is here is used to generate new files within `versions/`
- `versions/` - This directory holds the individual version scripts.


## Configuration

Inside the `alembic.ini` file, the following configuration is set:

```ini
sqlalchemy.url = postgresql://postgres:admin@localhost/test_db
```

`sqlalchemy.url` is the connection url for the PostgreSQL database. It follows the format:
  ```
  postgresql://username:password@host:port/database
  ```

In this case, it's:
- `username`: `postgres`
- `password`: `admin`
- `host`: `localhost`
- `database`: `test_db`

Then inside the `env.py` file, the following configuration is set:

```python
from app.database.database import Base
from app.database import *

...
target_metadata = Base.metadata
...
```
