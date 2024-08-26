# 1. API Versioning

This implementation is based on the [Postman Docs](https://www.postman.com/api-platform/api-versioning/)

## Introduction

`API` versioning is a way to manage changes to an `API`.
It allows for the `API` to evolve without breaking existing clients.
There are several ways to version an `API`, but the most common are:

1. **URL Path Versioning**: The version is included in the `URL` path.
2. **Query Parameter Versioning**: The version is included as a query parameter.
3. **Header Versioning**: The version is included in a header.

In this project, we will use `URL Path Versioning`.

## URL Path Versioning

In `URL Path Versioning`, the version is included in the `URL` path.

For example, the `URL` for the `API` version `0` might look like this:

```http
GET /api/v0/users
```

## Implementation

In the `main.py` entry point, we define the `API` version prefix as a constant:

```Python
prefix = '/api/v0'
```

Then we define the `API` routes with the prefix:

```Python
app.include_router(users.router, prefix=prefix)
app.include_router(user_types.router, prefix=prefix)
app.include_router(courses.router, prefix=prefix)
app.include_router(enrollments.router, prefix=prefix)
app.include_router(utility.router, prefix=prefix)
```

Now all the `API` routes will have the version prefix `/api/v0`.

Example for getting all users:

```http
GET localhost:8000/api/v0/users
```