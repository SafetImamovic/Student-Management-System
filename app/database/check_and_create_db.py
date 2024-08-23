import sys

from sqlalchemy import text, create_engine, Engine


def check_and_create_database(DB_USER: str, DB_PASS: str, DB_HOST: str, DB_PORT: str, DB_NAME: str) -> Engine:
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

    :param DB_USER:
    :param DB_PASS:
    :param DB_HOST:
    :param DB_PORT:
    :param DB_NAME:
    :return: Engine
    """

    default_database_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/"

    default_engine = create_engine(default_database_url, isolation_level="AUTOCOMMIT")

    try:
        with default_engine.connect() as connection:
            result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';"))

            exists = result.scalar() is not None

            if not exists:
                print(f"Database '{DB_NAME}' does not exist. Creating...")

                connection.execute(text(f"CREATE DATABASE {DB_NAME};"))

                print(f"Database '{DB_NAME}' created successfully.")

            else:
                print(f"Database '{DB_NAME}' already exists.")

        return create_engine(default_database_url + DB_NAME)

    except Exception as e:
        print(f"An error occurred while checking or creating the database: {e}")

        sys.exit(1)

    finally:
        default_engine.dispose(True)
