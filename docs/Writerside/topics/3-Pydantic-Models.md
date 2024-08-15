# 3. Pydantic Models

## Objective

Just like in the official [FastAPI docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models), to avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.

So a new file `schemas.py` will be created in the `app` directory.

## Pydantic Models

Pydantic models are used to define the structure of the data that will be received and returned by the API.

The general way of creating Pydantic models is to create a class that inherits from `BaseModel` from the `pydantic` module.

That class itself will act as a base class for all the Pydantic models that we will create.

e.g. we create a `UserBase` Pydantic model (or let's say "schema") to have common attributes while creating or reading data.

Then we create a `UserCreate` model that inherits from `UserBase` (so it will have the same attributes), plus any additional data (attributes) needed for creation.

So, the user will also have a password when creating it.

But for security, the password won't be in other Pydantic models, for example, it won't be sent from the API when reading a user.



```Python
from pydantic import BaseModel


```