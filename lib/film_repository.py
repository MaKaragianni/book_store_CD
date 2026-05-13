from lib.film import Film


class FilmRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute(
            "SELECT * FROM films"
        )

        films = []

        for row in rows:
            item = Film(
                row["id"],
                row["title"],
                row["director"]
            )

            films.append(item)

        return films
    
    def create(self, film): # accepts/inserts a Film object
        self._connection.execute(
            "INSERT INTO films (title, director) VALUES (%s, %s)",
            [film.title, film.director]
        )

        self._connection.commit()