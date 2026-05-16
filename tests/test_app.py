import sys
import os

# this line is a bit of a hack which allows us to import app without changing anything else
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# BOOKS API TESTS
# a descriptive test name
def test_get_books_returns_a_200():
    # here's where we make the test client
    client = app.test_client()

    # here's where we make the request
    response = client.get("/api/books")

    # here's where we assert that the response's status code is 200
    assert response.status_code == 200

# a descriptive test name
def test_get_books_returns_all_the_books():

    client = app.test_client()
    response = client.get("/api/books")

    # here's where we assert that the response body contains all the books
    # note that we need to call .json on the response
    assert response.json == [
      {"title": "The Gruffalo", "author": "Julia Donaldson"},
        {"title": "Ada Twist, Scientist", "author": "Andrea Beaty"},
        {"title": "The Girl Who Drank the Moon", "author": "Kelly Barnhill"},
        {"title": "Dragons in a Bag", "author": "Zetta Elliott"}
    ]

# AUTHORS API TESTS
def test_get_authors_returns_200():
    client = app.test_client()
    response = client.get("/api/authors")
    assert response.status_code == 200

def test_get_authors_returns_all_authors():
    client = app.test_client()
    response = client.get("/api/authors")
    assert response.json == [
        {"name": "Julia Donaldson", "dob": "1948-09-16"},
        {"name": "Andrea Beaty", "dob": "1961-10-08"},
        {"name": "Kelly Barnhill", "dob": "1973-01-01"},
        {"name": "Zetta Elliott", "dob": "1979-11-11"},
        {"name": "J.K. Rowling", "dob": "1965-07-31"}
    ]

# Quotes static page TESTS
def test_get_quotes_returns_200():
    client = app.test_client()
    response = client.get("/quotes")
    assert response.status_code == 200

def test_get_quotes_contains_quotes():
    client = app.test_client()
    response = client.get("/quotes")
    assert b"Books" in response.data

# SESSIONS & AUTHENTICATION TESTS
def test_get_login_form_returns_200():
    client = app.test_client()
    response = client.get("/sessions/new")
    assert response.status_code == 200


def test_login_successful_redirects_and_sets_session():
    # Create a dummy user inside the database so we have someone to authenticate
    from lib.database_connection import DatabaseConnection
    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()
    connection.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s);", 
        ["mario", "superpassword"]
    )

    client = app.test_client()
    
    # Submit the form values to /sessions
    response = client.post("/sessions", data={
        "username": "mario",
        "password": "superpassword"
    })

    # Assert it handles the successful routing
    assert response.status_code == 302
    assert response.location.endswith("/books")

    # Check that the session dictionary correctly populated the user information
    with client.session_transaction() as sess:
        assert sess["username"] == "mario"
        assert sess["user_id"] is not None


def test_login_failed_redirects_back_to_login_form():
    client = app.test_client()
    
    # Try logging in with a user profile that doesn't exist
    response = client.post("/sessions", data={
        "username": "im_not_real",
        "password": "wrong_password"
    })

    assert response.status_code == 302
    assert response.location.endswith("/sessions/new")