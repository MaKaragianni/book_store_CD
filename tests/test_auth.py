import sys
import os
from playwright.sync_api import Page, expect

# Allow imports from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from lib.database_connection import DatabaseConnection

# 1. INTEGRATION TESTS (Flask Test Client)
def test_auth_integration_success():
    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()
    connection.execute("TRUNCATE TABLE users RESTART IDENTITY;")
    connection.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ["test", "1234"])

    client = app.test_client()
    response = client.post('/sessions', data={
        'username': 'test',
        'password': '1234'
    })

    # Should redirect on success
    assert response.status_code == 302
    assert response.location.endswith("/books")


def test_auth_integration_failure():
    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()
    connection.execute("TRUNCATE TABLE users RESTART IDENTITY;")
    connection.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ["test", "1234"])

    client = app.test_client()
    response = client.post('/sessions', data={
        'username': 'test',
        'password': 'wrong_password_abc'
    })

    # Should redirect back to login page on failure
    assert response.status_code == 302
    assert response.location.endswith("/sessions/new")


# 2. END-TO-END BROWSER TESTS (Playwright)
def test_auth_playwright_success(page: Page):
    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()
    connection.execute("TRUNCATE TABLE users RESTART IDENTITY;")
    connection.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ["test", "1234"])
    DatabaseConnection.close_connection()

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill("1234")
    page.get_by_role("button", name="Log In").click()

    expect(page).to_have_url("http://127.0.0.1:5001/books")


def test_auth_playwright_failure(page: Page):
    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()
    connection.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ["test", "1234"])
    DatabaseConnection.close_connection()

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill("wrong_password")
    page.get_by_role("button", name="Log In").click()

    # User should be bounced right back to the login page form
    expect(page).to_have_url("http://127.0.0.1:5001/sessions/new")


def test_unauthenticated_user_cannot_create_book(page: Page):
    """Verify that an unauthenticated visitor trying to bypass 
    the UI and POST a book creation request gets kicked back to the login portal."""
    
    # We navigate straight to books page WITHOUT logging in
    page.goto("http://127.0.0.1:5001/books")
    
    # Try typing into the inputs and hitting submit
    page.get_by_placeholder("Title").fill("Stolen Book Data")
    page.get_by_placeholder("Author").fill("Hacker")
    page.get_by_role("button", name="Submit").click()

    # The @login_required decorator should catch this and redirect them to sign in
    expect(page).to_have_url("http://127.0.0.1:5001/sessions/new")