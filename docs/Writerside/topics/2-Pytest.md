# 2. Pytest

## Introduction

[`Pytest`](https://docs.pytest.org/) is a testing framework that simplifies
writing and executing test cases in Python.


## Installation

Before installing `Pytest`, we need to install `httpx`.

```bash
pip install httpx
```

Testing in FastAPI is based on HTTPX, which in turn is designed based on Requests,
so it's very familiar and intuitive.

To install `Pytest` run the following command:

```bash
pip install pytest
```

But because we are running the servers in Docker containers,
we just need to add them to the `requirements.txt`.

```text
httpx==0.27.2
pytest==8.3.2
```

These are the latest versions as of writing this document.

## How Does It Work

`Pytest` collects test cases from files and directories starting with `test_`.

Due to pytest’s detailed assertion introspection, only plain assert statements are used.

## Writing Test Cases

We will be following the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/testing/?h=pytest) on testing:

> A new directory `tests` will be created in the root of the project.

Test cases in `Pytest` are written as functions with names starting with `test_`.

To test the `users` endpoint, we can write a test case like this:

`tests/test_users.py`:
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_users():
    response = client.get("/api/v0/users/")
    assert response.status_code == 200

```

Explanation:

This Python code snippet demonstrates how to write a simple unit test for a FastAPI application using the `TestClient` from FastAPI's testing utilities. Here's an explanation of each part:

### 1. **Imports**
```python
from fastapi.testclient import TestClient
from main import app
```
- `TestClient`: This is a testing client provided by FastAPI, built on top of `requests`, allowing us to simulate requests to the FastAPI application as if it were running on a real server.
- `app`: This imports the FastAPI application instance from the `main.py` file, which is where the FastAPI app is defined.

### 2. **Creating the Test Client**
```python
client = TestClient(app)
```
- This line initializes the `TestClient` with the FastAPI app. This `client` will be used to send simulated HTTP requests to the application.

### 3. **Defining the Test Function**

```python
def test_read_users():
    response = client.get("/api/v0/users/")
    assert response.status_code == 200
```
- `test_read_users`: This is a test function. In Python, test functions typically start with the word `test_` to be recognized by test runners like `pytest`.
- `response = client.get("/api/v0/users/")`: This line sends a `GET` request to the `/api/v0/users/` endpoint of the FastAPI application using the `client`.
- `assert response.status_code == 200`: This assertion checks that the response status code is `200`, which indicates a successful request. If the status code is not `200`, the test will fail.

Then by running `pytest` in the terminal, the test will be executed, and the output will show if the test passed or failed.

> It does that by collecting all the files and directories starting with `test_` and running them.

The result will pass successfully, however, let's add another function to test the same route but assert that the response is a `404`:

```python
def test_read_users_fail():
    response = client.get("/api/v0/users/")
    assert response.status_code == 404
```

Then running `pytest -vv` will give us the following output:

> `-vv` is a flag that increases verbosity, showing more details about the tests as written [here](https://docs.pytest.org/en/stable/how-to/output.html).


```bash
tests/test_users.py::test_read_users PASSED                                                                                                    [ 50%]
tests/test_users.py::test_read_users_fail FAILED                                                                                               [100%]

===================================================================== FAILURES ====================================================================== 
_______________________________________________________________ test_read_users_fail ________________________________________________________________ 

    def test_read_users_fail():
        response = client.get("/api/v0/users/")
>       assert response.status_code == 404
E       assert 200 == 404
E        +  where 200 = <Response [200 OK]>.status_code

tests\test_users.py:14: AssertionError
```

This output shows that the first test passed, but the second test failed because the status code was `200` instead of `404`.
