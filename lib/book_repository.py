from lib.book import Book


class BookRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute(
            "SELECT * FROM books"
        )

        books = []

        for row in rows:
            item = Book(
                row["id"],
                row["title"],
                row["author"]
            )

            books.append(item)

        return books
    
    def create(self, book): # accepts/inserts a Book object
        self._connection.execute(
            "INSERT INTO books (title, author) VALUES (%s, %s)", # parameterised queries (%s placeholders) separate data from SQL structure.
            [book.title, book.author]
        )

        self._connection.commit()