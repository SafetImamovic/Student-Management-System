# 2. SQLAlchemy Models

The way we interact with databases in FastAPI is through SQLAlchemy models.

## Creating SQLAlchemy Models

To define SQLAlchemy models, we need to create Python classes that inherit from the
`Base` class provided by SQLAlchemy, as is done in week 1.

The `Base` class is the base class for all ORM models and maintains a catalog of
classes and tables relative to that base.

We first delete the Test table from the previous section and create three new tables:
`students`, `courses` and `enrollments`.

```python
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)

    enrollments = relationship('Enrollment', back_populates='student')


class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    enrollments = relationship('Enrollment', back_populates='course')


class Enrollment(Base):
    __tablename__ = 'enrollments'
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)

    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

```

In this code:
- `Student`, `Course`, and `Enrollment` are SQLAlchemy ORM models corresponding to the entities in the PlantUML diagram.
- Each model class inherits from `Base`, which is an instance of `declarative_base` provided by SQLAlchemy.
- Primary keys are marked with `primary_key=True` and are set to auto-increment.
- Foreign keys are specified using the `ForeignKey` class.
- Relationships between entities are defined using `relationship` to enable ORM features such as back-referencing.

## Migrating the Database

After defining the models, we need to create a migration script to apply these changes to the database.

We can use Alembic to generate migration scripts based on the changes in the models.

To create a migration script, run the following command:

```shell
alembic revision --autogenerate -m "create tables students, courses, enrollments"
```

This command generates a new migration script that creates the `students`, `courses`, and `enrollments` tables in the database.

The migration script is created in the `versions/` directory with a filename that includes a unique identifier.

```Bash
Safet@DESKTOP-24UA1HK ~/Desktop/Student-Management-System  database-setup alembic revision --autogenerate -m "create tables students, courses, enrollments"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'courses'
INFO  [alembic.autogenerate.compare] Detected added table 'students'
INFO  [alembic.autogenerate.compare] Detected added table 'enrollments'
Generating C:\Users\Safet\Desktop\Student-Management-System\alembic\versions\b3697945bdca_create_tables_students_courses_.py ...  done
```

Let's check the database to see if the tables have been created successfully.

After running `alembic upgrade head`:

```shell
student_management_system_db-# \d
                      List of relations
 Schema |             Name              |   Type   |  Owner
--------+-------------------------------+----------+----------
 public | alembic_version               | table    | postgres
 public | courses                       | table    | postgres
 public | courses_course_id_seq         | sequence | postgres
 public | enrollments                   | table    | postgres
 public | enrollments_enrollment_id_seq | sequence | postgres
 public | students                      | table    | postgres
 public | students_student_id_seq       | sequence | postgres
(7 rows)
```

If we take a look at the revision script, we can see the SQL commands that were executed:

<code-block lang="python" collapsible="true" collapsed-title="Migration Script">
<![CDATA[
"""create tables students, courses, enrollments

Revision ID: b3697945bdca
Revises:
Create Date: 2024-08-15 15:55:39.047273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3697945bdca'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
# ### commands auto generated by Alembic - please adjust! ###
op.create_table('courses',
sa.Column('course_id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('name', sa.String(), nullable=False),
sa.Column('description', sa.Text(), nullable=False),
sa.Column('start_date', sa.Date(), nullable=False),
sa.Column('end_date', sa.Date(), nullable=False),
sa.PrimaryKeyConstraint('course_id')
)
op.create_table('students',
sa.Column('student_id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('first_name', sa.String(), nullable=False),
sa.Column('last_name', sa.String(), nullable=False),
sa.Column('email', sa.String(), nullable=False),
sa.Column('age', sa.Integer(), nullable=False),
sa.PrimaryKeyConstraint('student_id'),
sa.UniqueConstraint('email')
)
op.create_table('enrollments',
sa.Column('enrollment_id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('student_id', sa.Integer(), nullable=False),
sa.Column('course_id', sa.Integer(), nullable=False),
sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
sa.PrimaryKeyConstraint('enrollment_id')
)
# ### end Alembic commands ###


def downgrade() -> None:
# ### commands auto generated by Alembic - please adjust! ###
op.drop_table('enrollments')
op.drop_table('students')
op.drop_table('courses')
# ### end Alembic commands ###
]]>

</code-block>