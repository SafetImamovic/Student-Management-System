default_users = [
    {
        "first_name": "Safet",
        "last_name": "Imamovic",
        "username": "admin",
        "email": "safet.imamovic.22@size.ba",
        "age": 21,
        "is_active": True,
        "user_type_id": 1,
        "hashed_password": "admin"
    },
    {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe123",
        "email": "john.doe@example.com",
        "age": 21,
        "is_active": True,
        "user_type_id": 2,
        "hashed_password": "password1"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "username": "janedoe69",
        "email": "jane.smith@example.com",
        "age": 22,
        "is_active": True,
        "user_type_id": 2,
        "hashed_password": "password2"
    }
]


default_courses = [
    {
        "name": "Python 101",
        "description": "Basic Python",
        "start_date": "2024-08-17",
        "end_date": "2024-08-17",
        "is_active": True
    },
    {
        "name": "Alembic 101",
        "description": "World Database Migration",
        "start_date": "2024-08-17",
        "end_date": "2024-08-17",
        "is_active": True
    },
]


default_enrollments = [
    {
      "enrolled_date": "2024-08-17",
      "end_date": "2024-08-17",
      "associative_data": "Associative Data Relative To John and Python 101",
      "user_id": 2,
      "course_id": 1
    },
    {
      "enrolled_date": "2024-08-17",
      "end_date": "2024-08-17",
      "associative_data": "Associative Data Relative To John and Alembic 101",
      "user_id": 2,
      "course_id": 2
    },
    {
      "enrolled_date": "2024-08-17",
      "end_date": "2024-08-17",
      "associative_data": "Associative Data Relative To Jane and Alembic 101",
      "user_id": 3,
      "course_id": 1
    }
]
