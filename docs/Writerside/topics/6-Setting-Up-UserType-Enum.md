# 7. Seeding DB Records

As mentioned earlier there will not be a `students` table, rather a `users` table with a 
discriminator column `user_type` to differentiate between students, teachers and even other types.

Because of this there must be at least one `user_type` in the `users` table
to enable User creation. This is where seeding comes in.

## Seeding the Tables

In the `crud.py` file in the `app` directory, the following code to seed the tables is added:

```Python
import app.database.schemas.enrollments
import app.database.schemas.courses
import app.database.schemas.users

import app.database.schemas.user_types


def seed_user_types(db: Session):
    """
    This function seeds the user_types table with some initial values
    :param db:
    :return:
    """
    if db.query(app.database.schemas.user_types.UserType).count() == 0:
        reset_auto_increment(db, 'user_types', 'user_type_id')

        default_user_types = ['Admin', 'Student']

        # results = []

        for user_type in default_user_types:
            db.add(app.database.schemas.user_types.UserType(name=user_type))
        db.commit()


def seed_users(db: Session):
    """
    This function seeds the users table with some initial values
    :param db:
    :return:
    """
    if db.query(app.database.schemas.users.User).count() == 0:
        reset_auto_increment(db, 'users', 'user_id')

        for user in default_users:
            db.add(app.database.schemas.users.User(**user))
        db.commit()


def seed_courses(db: Session):
    """
    This function seeds the courses table with some initial values
    :param db:
    :return:
    """
    if db.query(app.database.schemas.courses.Course).count() == 0:
        reset_auto_increment(db, 'courses', 'course_id')

        for course in default_courses:
            db.add(app.database.schemas.courses.Course(**course))
        db.commit()


def seed_enrollments(db: Session):
    """
    This function seeds the enrollments table with some initial values
    :param db:
    :return:
    """
    if db.query(app.database.schemas.enrollments.Enrollment).count() == 0:

        for enrollment in default_enrollments:
            db.add(app.database.schemas.enrollments.Enrollment(**enrollment))
        db.commit()


def seed(db: Session):
    seed_user_types(db)
    seed_users(db)
    seed_courses(db)
    seed_enrollments(db)
```

This seeds the `user_types` table with the default user types `Admin` and `Student`.

This also seeds the `users`, `courses`, and `enrollments` tables with default values.

`reset_auto_increment`: This function takes the db session, table_name, and column_name as arguments and executes a raw SQL command to reset the sequence for the specified table and column.

`seed_user_types`: Checks if the user_types table is empty, resets the auto-increment counter, and then seeds the table with default user types.

`main.py`:

```Python
@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    seed(db)
    db.close()
```

