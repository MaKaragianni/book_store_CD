class Book:
    def __init__(self, id, title, author):
        title = title.strip()
        author = author.strip()

        if not title or not isinstance(title, str):
            raise ValueError("Book title must be a non-empty string")

        if not author or not isinstance(author, str):
            raise ValueError("Book author must be a non-empty string")

        if len(title) > 255:
            raise ValueError("Book title too long")

        if len(author) > 255:
            raise ValueError("Book author too long")

        self.id = id
        self.title = title
        self.author = author

    def __repr__(self):
        return f"Book({self.id}, {self.title}, {self.author})"
    