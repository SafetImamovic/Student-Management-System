# 6. Seeding DB Records

As mentioned earlier there will not be a `students` table, rather a `users` table with a 
discriminator column `user_type` to differentiate between students, teachers and even other types.

Because of this there must be at least one `user_type` in the `users` table
to enable User creation. This is where seeding comes in.

## Seeding the `user_types` Table

In the `crud.py` file in the `app` directory, the following code to seed the `user_types` table is added:

```Python
def reset_auto_increment(db: Session, table_name: str, column_name: str):
    # alter sequence user_types_user_type_id_seq restart with 1;
    reset_sql = text(f"alter sequence {table_name}_{column_name}_seq restart with 1")
    db.execute(reset_sql)
    db.commit()


def seed_user_types(db: Session):
    if db.query(models.UserType).count() == 0:
        reset_auto_increment(db, 'user_types', 'user_type_id')

        default_user_types = ['Admin', 'Student']

        for user_type in default_user_types:
            db.add(models.UserType(name=user_type))
        db.commit()
```

This seeds the `user_types` table with the default user types `Admin` and `Student`.

`reset_auto_increment`: This function takes the db session, table_name, and column_name as arguments and executes a raw SQL command to reset the sequence for the specified table and column.

`seed_user_types`: Checks if the user_types table is empty, resets the auto-increment counter, and then seeds the table with default user types.

`main.py`:

```Python
@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    crud.seed_user_types(db)
    db.close()
```

## Seeding the `users` Table

In the `crud.py` file in the `app` directory, the following code to seed the `users` table is added:

```Python