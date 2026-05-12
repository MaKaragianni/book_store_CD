import os
from psycopg import connect
from psycopg.rows import dict_row

DATABASE_NAME = os.getenv("DATABASE_NAME", "book_store_test")

class DatabaseConnection:
    _connection = None

# Connection set for Docker/EC2:
#    @classmethod
#    def connect(cls):
#        cls._connection = connect(
#            "postgresql://postgres:password@book_store_db/book_store",
#            row_factory=dict_row
#        )

# Connection set locally:
    @classmethod
    def connect(cls):
        cls._connection = connect(
            f"postgresql://localhost/{DATABASE_NAME}",
            row_factory=dict_row,
            autocommit=True
        )

    @classmethod
    def get_connection(cls):
        return cls._connection
    

    @classmethod
    def seed(cls, sql_filename):
        connection = cls.get_connection()

        with open(sql_filename, "r") as file:
            sql = file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql)