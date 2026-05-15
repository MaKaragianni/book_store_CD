from lib.database_connection import DatabaseConnection
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001")

    h1 = page.locator("h1")

    expect(h1).to_have_text("Welcome to AceReads!")

def test_books_page_has_heading(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    h1 = page.locator("h1")

    expect(h1).to_have_text("Our Books")

def test_book_list_contains_all_books(page: Page):

    DatabaseConnection.connect()

    DatabaseConnection.seed("./seeds/books.sql")

    DatabaseConnection.close_connection()

    page.goto("http://127.0.0.1:5001/books")

    books = page.locator('.book-card')

    expected_books = [
      'The Gruffalo\n\nJulia Donaldson',
      'Ada Twist, Scientist\n\nAndrea Beaty',
      'The Girl Who Drank the Moon\n\nKelly Barnhill',
      'Dragons in a Bag\n\nZetta Elliott'
    ]

    actual_books = books.all_inner_texts()

    assert actual_books == expected_books

def test_films_list_contains_all_films(page: Page):
    DatabaseConnection.connect()
    DatabaseConnection.seed("./seeds/films.sql")
    DatabaseConnection.close_connection()

    page.goto("http://127.0.0.1:5001/films")

    h1 = page.locator("h1")

    expect(h1).to_have_text("Our Films")

    films = page.locator('.film-card')

    expected_films = [
      'Mortal Kombat II\n\nSimon McQuoid',
      'The Devil Wears Prada 2\n\nDavid Frankel',
      'Oppenheimer\n\nChristopher Nolan',
      'Project Hail Mary\n\nPhil Lord'
    ]

    actual_films = films.all_inner_texts()

    assert actual_films == expected_films

def test_can_create_a_new_book(page: Page):
    DatabaseConnection.connect()
    DatabaseConnection.seed("./seeds/books.sql")
    connection = DatabaseConnection.get_connection()
    connection.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ["test", "1234"])
    DatabaseConnection.close_connection()

    # Go to the login page first and authenticate
    page.goto("http://127.0.0.1:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill("1234")
    page.get_by_role("button", name="Log In").click()

    # Now that Playwright has the session cookie, proceed to create the book
    page.goto("http://127.0.0.1:5001/books")

    page.get_by_placeholder("Title").fill("The Chronicles of Geronimo (the cat)")
    page.get_by_placeholder("Author").fill("Geronimo")

    page.get_by_role("button", name="Submit").click()

    expect(page.locator("body")).to_contain_text("The Chronicles of Geronimo (the cat)")

    expect(page.locator("body")).to_contain_text("Geronimo")

def test_can_create_a_new_film(page: Page):
    DatabaseConnection.connect()
    DatabaseConnection.seed("./seeds/films.sql")
    connection = DatabaseConnection.get_connection()
    connection.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ["test", "1234"])
    DatabaseConnection.close_connection()

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill("1234")
    page.get_by_role("button", name="Log In").click()

    page.goto("http://127.0.0.1:5001/films")

    page.get_by_placeholder("Title").fill("Interstellar")
    page.get_by_placeholder("Director").fill("Christopher Nolan")

    page.get_by_role("button", name="Submit").click()

    expect(page.locator("body")).to_contain_text("Interstellar")

    expect(page.locator("body")).to_contain_text("Christopher Nolan")


def test_can_sign_up_new_user(page: Page):
    page.goto("http://127.0.0.1:5001/users/new")

    page.get_by_placeholder("username").fill("newuser123")
    page.get_by_placeholder("password").fill("securepass")

    page.get_by_role("button", name="Sign Up").click()

    # should redirect to books page
    expect(page).to_have_url("http://127.0.0.1:5001/books")

    # confirm page still works after signup
    expect(page.locator("h1")).to_have_text("Our Books")


def test_can_log_in_existing_user(page: Page):
    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()
    connection.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s);", 
        ["auth_user", "mypass123"]
    )
    DatabaseConnection.close_connection()

    page.goto("http://127.0.0.1:5001/sessions/new")

    page.locator("#username").fill("auth_user")
    page.locator("#password").fill("mypass123")

    page.get_by_role("button", name="Log In").click()

    expect(page).to_have_url("http://127.0.0.1:5001/books")
    expect(page.locator("h1")).to_have_text("Our Books")