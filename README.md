# AceBooks - Book Store App

A full-stack Flask web application that allows users to view and create books stored in a PostgreSQL database.

The project includes:

End-to-end testing with Playwright
Pytest-based integration testing
Automatic Flask server startup during tests
Database seeding for test isolation
Environment-based configuration for development and testing

---

## Features

### Books
- View all books stored in PostgreSQL
- Add new books via HTML form
- Books rendered using Flask + Jinja templates

### Films
- View list of films and directors
- Add new films via HTML form
- Film data stored in PostgreSQL database

### Authors Page
- Static list of authors with birth dates
- Displays dynamic Jinja templating

### Quotes Page
- Static inspirational reading quotes

### Team Page
- Simple team page using Jinja loops

## Testing Strategy
This project uses two layers of testing:

1. Integration + API Tests (pytest)
    - Flask server is automatically started using conftest.py
    - Tests send real HTTP requests to http://127.0.0.1:5001
    - Database is seeded before tests run

2. End-to-End UI Tests (Playwright)
    - Simulates real user interaction in browser
    - Tests pages, forms, and UI updates

---

## Test Infrastructure
Automatic Flask Server Startup

Tests use tests/conftest.py to:
    - Start Flask in a subprocess
    - Wait until /books endpoint is available
    - Run all tests
    - Shut down server after completion

This ensures:

    Tests always run against a real, live server

---

## Database Seeding

Before tests run, SQL seed files are executed to reset state.

This ensures:
    - Clean database for every test run
    - Predictable test data
    - No dependency between tests

---

## SQL Execution Behavior

Seed files are executed statement-by-statement:
    - SQL file is split using ;
    - Each statement is executed individually
    - Empty statements are ignored

This allows safe execution of multi-query seed files.

---

## Tech Stack

- Python 3.13
- Flask
- PostgreSQL
- psycopg (PostgreSQL driver)
- Jinja2 templates
- Playwright (browser testing)
- Pytest
- Docker (optional)
- HTML/CSS (SimpleCSS CDN)

---

## Project Structure

book_store/
│
├── app.py
├── lib/
│   ├── database_connection.py
│   ├── book_repository.py
│   ├── film_repository.py
│   ├── book.py
│   ├── film.py
│
├── templates/
│   ├── books.html
│   ├── films.html
│   ├── index.html
│   ├── authors.html
│   ├── quotes.html
│   ├── team.html
│
├── seeds/
│   └── books.sql
│   └── films.sql
│
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_landing_page.py
│
├── book_store_venv/ (Not included on GitHub project)
├── Dockerfile
├── requirements.txt
├── README.md


---

## Database Setup

### Create databases

```sql
CREATE DATABASE book_store;
CREATE DATABASE book_store_test;
```

#### Tables

Books

```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT
);
```

Films

```sql
CREATE TABLE films (
    id SERIAL PRIMARY KEY,
    title TEXT,
    director TEXT
);
```

#### Database Seeding

The database is reset before tests using SQL seed files.

books.sql
- Truncates table
- Inserts test data

```sql
TRUNCATE TABLE books RESTART IDENTITY CASCADE;

INSERT INTO books (title, author)
VALUES ('The Gruffalo', 'Julia Donaldson');
```

films.sql
- Truncates table
- Inserts test data

```sql
TRUNCATE TABLE films RESTART IDENTITY CASCADE;

INSERT INTO films (title, director)
VALUES ('Mortal Kombat II', 'Simon McQuoid');
```

#### Environment Configuration

The app supports switching databases using environment variables:

DATABASE_NAME=book_store python app.py

The test suite uses a separate database:

book_store_test

Configured in:

lib/database_connection.py

---

## Running Tests

Run all tests:

pytest

Run with verbose output:

pytest -sv


#### Test Requirements

Before running tests ensure:
    - Flask server is NOT manually started (handled by conftest.py)
    - book_store_test database exists
    - Seed files are correct
    - Environment variables are set in .env


---

## Playwright Testing

Tests simulate real user behaviour:

Example:
Navigate to /books
Fill form fields
Submit form
Verify UI updates

page.get_by_placeholder("Title").fill("Harry Potter")
page.get_by_role("button", name="Submit").click()

---

## Running the App

Start server:

python app.py

Then visit:

http://127.0.0.1:5001/


---

## Docker Setup (optional)

Build image:

docker build -t book-store-app .

Run container:

docker run -p 5001:5001 book-store-app

---

### requirements.txt

Key dependencies:

Flask
psycopg
pytest
playwright
requests

(Full list included in repo)

---

## Key Learning Outcomes:
Flask routing (GET + POST)
HTML form handling
Jinja templating
PostgreSQL CRUD operations
Repository pattern (clean architecture)
Test-driven development (TDD)
End-to-end testing with Playwright
Database seeding for test isolation
Subprocess-based test servers
Environment-based configuration
Docker containerisation
Pytest fixtures and automated test infrastructure

---

## Test Strategy:
Integration tests → real Flask server + PostgreSQL database
UI tests → real browser automation
Test DB is fully reset via seed files
Full browser tests with Playwright
Independent test database (book_store_test)
Server lifecycle managed via conftest.py

Built as part of a full-stack Python training project using Flask, PostgreSQL, and Playwright testing.