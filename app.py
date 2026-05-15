from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv

from lib.database_connection import DatabaseConnection
from lib.book_repository import BookRepository
from lib.film_repository import FilmRepository
from lib.user_repository import UserRepository
from lib.book import Book
from lib.film import Film
from lib.user import User


load_dotenv()

app = Flask(__name__)
app.secret_key = "some_really_secret_key"

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


# Login Form
@app.route('/sessions/new', methods=['GET'])
def get_login_form():
    return render_template("login_form.html")


@app.route('/sessions', methods=['POST'])
def create_session():
    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()
    user_repository = UserRepository(connection)

    # Grab the data the user typed into the form inputs
    username = request.form["username"]
    password = request.form["password"]

    # Search for the user in the database
    user = user_repository.find_by_username(username)

    # Verify if the user exists AND the plain-text passwords match
    if user and user.password == password:
        # Success! Save data into Flask's session dictionary
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/books")
    else:
        # Failure! Send them back to the login page to try again
        return redirect("/sessions/new")


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


@app.route('/users/new', methods=['GET']) # Displays page/form
def get_signup_form():
    return render_template("signup_form.html")


@app.route('/users', methods=['POST']) # Processes submitted data
def create_user():

    DatabaseConnection.connect()

    connection = DatabaseConnection.get_connection()
    repository = UserRepository(connection)

    username = request.form['username'].strip() # Gets submitted form data
    password = request.form['password'].strip()

    user = User(username, password) # Creates a Python object

    repository.create(user)

    return redirect('/books')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    