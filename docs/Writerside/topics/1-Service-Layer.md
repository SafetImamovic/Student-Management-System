# 1. Service Layer

This implementation is based on the [Martin Fowler's Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html)

## Introduction

The **Service Layer** is a design pattern that defines an application's boundary
with a layer of services that establishes a set of available operations.

It encapsulates the application's business logic, controlling transactions,
and coordinating responses in the implementation of its operations.

In this project, we will implement a Service Layer to manage the business logic

## Flow

<code-block lang="mermaid">
graph TD
    Client -->|HTTP Request| A
    A[Router] -->|Calls method, Depends on UserController| B[Controller]
    B -->|Calls UserService method and passes the Session| C[Service]
    C -->|Calls the SQLAlchemy CRUD session methods| D[Model]
    D -->|Returns result or raises Exception| C
    C -->|Returns result| B
    B -->|Returns result| A
    A -->|Returns JSON response| Client
</code-block>

**Explanation**:
1. Router:

   The entry point for incoming HTTP requests.
   Directs requests to the appropriate controller based on the route.

2. Controller:

   Contains the logic for handling requests.
   Depends on services to perform operations.
   Forwards the result from the service back to the router.

3. Service:

   Contains the business logic.
   Interacts with the model to perform CRUD operations or other business logic.

4. Model:

   Represents the database entities.
   Used by the service to interact with the database.

<procedure>
<p>Example of getting the count of users in the database:</p>

<code-block lang="mermaid">
graph TD
    Client -->|HTTP Request| A
    A[users Router] -->|Calls get_count, Depends on UserController| B[UserController]
    B -->|Calls UserService get_count and passes the Session| C[UserService]
    C -->|Calls the SQLAlchemy count session methods| D[UserModel]
    D -->|Returns int or raises Exception| C
    C -->|Returns int| B
    B -->|Returns int| A
    A -->|Returns JSON response| Client
</code-block>
</procedure>




## Implementation

In the `service` directory, we define the service classes for the application.

For example, the `UserService` class looks like this:

```python
imports {...}

class UserService:
    @staticmethod
    def get_count(session: Session) -> int:
        return session.query(User).count()
...
```

Static methods in Python are used when a method doesn't need to access or modify the instance 
(i.e., it doesn't need to access self or the class itself via cls). 

In other words, static methods are used when the behavior defined in the method 
is related to the class but doesn't require any instance-specific data.

## Example

All the way from `main.py`:

```python
...
app.include_router(users.router, prefix=prefix)
...
```

To `users.py` in the `routers` module:

```python
@router.get(
    '/count/',
    responses={

    },
    response_model=int
)
def get_count(
    controller: Annotated[UserController, Depends(UserController)]
):
    """
    This function returns the number of users in the database
    :param controller: UserController Dependency
    :return: The number of users in the database
    """

    return controller.get_count()
```

To `UserController` in the `controllers` module:

```python
...
class UserController(BaseController):
    def get_count(self) -> int:
        """
        This method returns the number of users in the database
        :return:
        """

        return UserService.get_count(self.session)
...
```

To `UserService` in the `services` module:

```python
...
class UserService:
    @staticmethod
    def get_count(session: Session) -> int:
        return session.query(User).count()
...
```

To `User` in the `models` module (not shown here).

This is how the Service Layer is implemented in the project.