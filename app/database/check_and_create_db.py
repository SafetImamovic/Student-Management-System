import sys

from sqlalchemy import text, create_engine, Engine


def check_and_create_database(db_user: str, db_pass: str, db_host: str, db_port: str, db_name: str) -> Engine:
    """
    This function creates the database if it does not exist.

    It does that by creating a default engine (engine without a direct connection to a specific database).

    Sets the isolation_level="AUTOCOMMIT" during it's instantiation.

    PostgreSQL does not allow CREATE DATABASE to be executed within a transaction block.
    This means we cannot use BEGIN and COMMIT or ROLLBACK for these operations.
    The CREATE DATABASE command needs to be run immediately and independently of other
    database changes.

    It then checks the PSQL database catalogue (pg_database) for the correct database name.

    If it does not exist, it creates it, then creates the Engine instance connecting to the
    database and returns the Engine.

    If it does exist, it does nothing.

    Finally, it disposes of the default connection and returns the Engine.

    :param db_user:
    :param db_pass:
    :param db_host:
    :param db_port:
    :param db_name:
    :return:
    """

    default_database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/"

    default_engine = create_engine(default_database_url, isolation_level="AUTOCOMMIT")

    try:
        with default_engine.connect() as connection:
            result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}';"))

            exists = result.scalar() is not None

            if not exists:
                print(f"Database '{db_name}' does not exist. Creating...")

                connection.execute(text(f"CREATE DATABASE {db_name};"))

                print(f"Database '{db_name}' created successfully.")

            else:
                print(f"Database '{db_name}' already exists.")

        return create_engine(default_database_url + db_name)

    except Exception as e:
        print(f"An error occurred while checking or creating the database: {e}")

        sys.exit(1)

    finally:
        default_engine.dispose(True)
