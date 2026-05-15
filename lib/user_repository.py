from lib.user import User

class UserRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Create a new user and insert data into PostgreSQL

    def create(self, user):
        self._connection.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            [user.username, user.password]
        )
        return None

