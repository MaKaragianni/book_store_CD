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

    # Before the server can verify a password, it has to find the user in the database by their username.
    def find_by_username(self, username):
        cursor = self._connection.execute(
            'SELECT * FROM users WHERE username = %s', [username]
        )
        # Fetch all matching rows from the database cursor stream
        rows = cursor.fetchall()
        
        # Safe check: if no user is found with that username, return None
        if not rows:
            return None
        
        user_details = rows[0]
        return User(
            user_details["username"],
            user_details["password"],
            user_details["id"]
        )