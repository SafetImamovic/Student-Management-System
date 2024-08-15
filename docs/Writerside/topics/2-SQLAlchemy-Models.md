# 2. SQLAlchemy Models

The way we interact with databases in FastAPI is through SQLAlchemy models.

## Creating SQLAlchemy Models

To define SQLAlchemy models, we need to create Python classes that inherit from the
`Base` class provided by SQLAlchemy, as is done in week 1.

The `Base` class is the base class for all ORM models and maintains a catalog of
classes and tables relative to that base.

We first delete the `Test` model from the previous section and create 4 new models:
1. `Users`
2. `UserTypes`
3. `Courses`
4. `Enrollments`

<code-block lang="python" collapsed-title="models.py" collapsible="true">
<![CDATA[
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class UserType(Base):
__tablename__ = 'user_types'

    user_type_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String(50), nullable=False, unique=True)

    users = relationship('User', back_populates='user_type')

class User(Base):
__tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, CheckConstraint('age > 0'), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_type_id = Column(Integer, ForeignKey('user_types.user_type_id'), nullable=False)

    user_type = relationship('UserType', back_populates='users')
    enrollments = relationship('Enrollment', back_populates='user')

    __table_args__ = (
        UniqueConstraint('email', name='uq_users_email'),
    )

class Course(Base):
__tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)

    enrollments = relationship('Enrollment', back_populates='course')

class Enrollment(Base):
__tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    enrolled_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    associative_data = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)

    user = relationship('User', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

]]>

</code-block>>

In this code:
- We define the `UserType`, `User`, `Course`, and `Enrollment` models.
- We define the columns for each model using the `Column` class from SQLAlchemy.
- We define the relationships between the models using the `relationship` function from SQLAlchemy.
- We define the constraints for the columns using the `CheckConstraint` and `UniqueConstraint` classes from SQLAlchemy.
- We define the table name for each model using the `__tablename__` attribute.
- We define the primary key for each model using the `primary_key=True` argument.
- We define the foreign key relationships between the models using the `ForeignKey` class from SQLAlchemy.
- We define the default values for the columns using the `default` argument.

## Migrating the Database

After defining the models, we need to create a migration script to apply these changes to the database.

We can use Alembic to generate migration scripts based on the changes in the models.

To create a migration script, run the following command:

```shell
alembic revision --autogenerate -m "create tables users, user_types, courses, enrollments"
```

This command generates a migration script that creates the tables `users`, `user_types`, `courses`, and `enrollments` in the database.

The migration script is created in the `versions/` directory with a filename that includes a unique identifier.

```Bash
Safet@DESKTOP-24UA1HK ~/Desktop/Student-Management-System  database-setup alembic revision --autogenerate -m "create tables users, user_types, courses, enrollments"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'courses'
INFO  [alembic.autogenerate.compare] Detected added table 'user_types'
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'enrollments'
Generating C:\Users\Safet\Desktop\Student-Management-System\alembic\versions\1c2b6b152893_create_tables_users_user_types_courses_.py ...  done
```

Let's check the database to see if the tables have been created successfully.

After running `alembic upgrade head`:

```shell
student_management_system_db=# \d
                      List of relations
 Schema |             Name              |   Type   |  Owner
--------+-------------------------------+----------+----------
 public | alembic_version               | table    | postgres
 public | courses                       | table    | postgres
 public | courses_course_id_seq         | sequence | postgres
 public | enrollments                   | table    | postgres
 public | enrollments_enrollment_id_seq | sequence | postgres
 public | user_types                    | table    | postgres
 public | user_types_user_type_id_seq   | sequence | postgres
 public | users                         | table    | postgres
 public | users_user_id_seq             | sequence | postgres
(9 rows)
```

If we take a look at the revision script, we can see the SQL commands that were executed:

<code-block lang="python" collapsible="true" collapsed-title="Migration Script">
<![CDATA[
"""create tables users, user_types, courses, enrollments

Revision ID: 1c2b6b152893
Revises:
Create Date: 2024-08-15 18:15:03.930775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c2b6b152893'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
# ### commands auto generated by Alembic - please adjust! ###
op.create_table('courses',
sa.Column('course_id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('name', sa.String(length=100), nullable=False),
sa.Column('description', sa.Text(), nullable=True),
sa.Column('start_date', sa.Date(), nullable=False),
sa.Column('end_date', sa.Date(), nullable=False),
sa.Column('created_at', sa.DateTime(), nullable=True),
sa.Column('updated_at', sa.DateTime(), nullable=True),
sa.Column('is_active', sa.Boolean(), nullable=False),
sa.PrimaryKeyConstraint('course_id')
)
op.create_table('user_types',
sa.Column('user_type_id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('created_at', sa.DateTime(), nullable=True),
sa.Column('updated_at', sa.DateTime(), nullable=True),
sa.Column('name', sa.String(length=50), nullable=False),
sa.PrimaryKeyConstraint('user_type_id'),
sa.UniqueConstraint('name')
)
op.create_table('users',
sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('first_name', sa.String(length=50), nullable=False),
sa.Column('last_name', sa.String(length=50), nullable=False),
sa.Column('email', sa.String(length=100), nullable=False),
sa.Column('age', sa.Integer(), nullable=True),
sa.Column('is_active', sa.Boolean(), nullable=False),
sa.Column('created_at', sa.DateTime(), nullable=True),
sa.Column('updated_at', sa.DateTime(), nullable=True),
sa.Column('last_login', sa.DateTime(), nullable=True),
sa.Column('user_type_id', sa.Integer(), nullable=False),
sa.ForeignKeyConstraint(['user_type_id'], ['user_types.user_type_id'], ),
sa.PrimaryKeyConstraint('user_id'),
sa.UniqueConstraint('email'),
sa.UniqueConstraint('email', name='uq_users_email')
)
op.create_table('enrollments',
sa.Column('enrollment_id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('enrolled_date', sa.DateTime(), nullable=True),
sa.Column('end_date', sa.DateTime(), nullable=True),
sa.Column('updated_at', sa.DateTime(), nullable=True),
sa.Column('associative_data', sa.Text(), nullable=True),
sa.Column('user_id', sa.Integer(), nullable=False),
sa.Column('course_id', sa.Integer(), nullable=False),
sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
sa.PrimaryKeyConstraint('enrollment_id')
)
# ### end Alembic commands ###


def downgrade() -> None:
# ### commands auto generated by Alembic - please adjust! ###
op.drop_table('enrollments')
op.drop_table('users')
op.drop_table('user_types')
op.drop_table('courses')
# ### end Alembic commands ###

]]>

</code-block>

