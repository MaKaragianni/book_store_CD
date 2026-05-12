class Film:
    def __init__(self, id, title, director):
        self.id = id
        self.title = title
        self.director = director

    def __repr__(self):
        return f"Film({self.id}, {self.title}, {self.director})"