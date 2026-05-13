class Film:
    def __init__(self, id, title, director):
        title = title.strip()
        director = director.strip()

        if not title or not isinstance(title, str):
            raise ValueError("Film title must be a non-empty string")

        if not director or not isinstance(director, str):
            raise ValueError("Film director must be a non-empty string")

        if len(title) > 255:
            raise ValueError("Film title too long")

        if len(director) > 255:
            raise ValueError("Film director too long")

        self.id = id
        self.title = title
        self.director = director

    def __repr__(self):
        return f"Film({self.id}, {self.title}, {self.director})"