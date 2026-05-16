import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    CONNECTION = None

    @classmethod
    def connect(cls):
        cls.CONNECTION = psycopg.connect(
            host=os.getenv("DATABASE_HOST"),
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            port=os.getenv("DATABASE_PORT"),
            row_factory=dict_row
        )

        cls.CONNECTION.autocommit = True # Every SQL statement is saved immediately. No manual COMMIT needed.

    @classmethod
    def get_connection(cls):
        return cls.CONNECTION

    @classmethod
    def seed(cls, sql_filename):
        connection = cls.get_connection()

        with open(sql_filename, "r") as file:
            sql = file.read()

        with connection.cursor() as cursor:
            for statement in sql.split(";"): # process each piece one by one
                stmt = statement.strip() # Remove whitespace
                if stmt: # skip empty statements
                    cursor.execute(stmt) # Each SQL statement runs separately
            #cursor.execute(sql)

        connection.commit()

    @classmethod # After each seed, close the connection
    def close_connection(cls):
        if cls.CONNECTION:
            cls.CONNECTION.close()
            cls.CONNECTION = None 