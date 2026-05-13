from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

from lib.database_connection import DatabaseConnection
from lib.book_repository import BookRepository
from lib.film_repository import FilmRepository
from lib.book import Book
from lib.film import Film

load_dotenv()

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello to you too"


# HTML ROUTES

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/books', methods=['GET'])
def get_books():

    DatabaseConnection.connect()

    connection = DatabaseConnection.get_connection()
    repository = BookRepository(connection)

    books = repository.all()

    return render_template("books.html", books=books)


@app.route('/films', methods=['GET'])
def get_films():

    DatabaseConnection.connect()

    connection = DatabaseConnection.get_connection()
    repository = FilmRepository(connection)

    films = repository.all()

    return render_template("films.html", films=films)


@app.route('/authors', methods=['GET'])
def get_authors():
    authors = [
        {"name": "Julia Donaldson", "dob": "1948-09-16"},
        {"name": "Andrea Beaty", "dob": "1961-10-08"},
        {"name": "Kelly Barnhill", "dob": "1973-01-01"},
        {"name": "Zetta Elliott", "dob": "1979-11-11"},
        {"name": "J.K. Rowling", "dob": "1965-07-31"}
    ]

    return render_template("authors.html", authors=authors)


@app.route('/quotes', methods=['GET'])
def get_quotes():
    return render_template("quotes.html")


@app.route('/team', methods=['GET'])
def get_team():
    team = ["Dorothy", "Rose", "Blanche", "Sophia"]
    return render_template("team.html", team=team)


# API ROUTES

@app.route('/api/authors', methods=['GET'])
def api_authors():
    return [
        {"name": "Julia Donaldson", "dob": "1948-09-16"},
        {"name": "Andrea Beaty", "dob": "1961-10-08"},
        {"name": "Kelly Barnhill", "dob": "1973-01-01"},
        {"name": "Zetta Elliott", "dob": "1979-11-11"},
        {"name": "J.K. Rowling", "dob": "1965-07-31"}
    ]


@app.route('/api/books', methods=['GET'])
def api_books():
    return [
        {"title": "The Gruffalo", "author": "Julia Donaldson"},
        {"title": "Ada Twist, Scientist", "author": "Andrea Beaty"},
        {"title": "The Girl Who Drank the Moon", "author": "Kelly Barnhill"},
        {"title": "Dragons in a Bag", "author": "Zetta Elliott"}
    ]


@app.route('/books', methods=['POST'])
def create_book():

    DatabaseConnection.connect()

    connection = DatabaseConnection.get_connection()
    repository = BookRepository(connection)

    title = request.form["title"].strip()
    author = request.form["author"].strip()

    book = Book(None, title, author)

    repository.create(book)

    return redirect("/books")


@app.route('/films', methods=['POST'])
def create_film():

    DatabaseConnection.connect()

    connection = DatabaseConnection.get_connection()
    repository = FilmRepository(connection)

    title = request.form["title"].strip()
    director = request.form["director"].strip()

    film = Film(None, title, director)

    repository.create(film)

    return redirect("/films")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)