class User:
    def __init__(self, username, password, id=None):

        username = username.strip()
        password = password.strip()

        if username == "":
            raise ValueError("Username cannot be empty")

        if password == "":
            raise ValueError("Password cannot be empty")

        if len(username) > 255:
            raise ValueError("Username too long")

        if len(password) > 255:
            raise ValueError("Password too long")

        self.id = id
        self.username = username
        self.password = password