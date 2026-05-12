# AceBooks - Book Store App

A full-stack Flask web application that allows users to view and create books stored in a PostgreSQL database.
The project includes automated end-to-end testing using Playwright, database seeding and environment-based configuration for development and testing.

---

## Features

### Books
- View all books stored in PostgreSQL
- Add new books via HTML form
- Books rendered using Flask + Jinja templates

### Films
- View list of films and directors
- Film data stored in PostgreSQL

### Authors Page
- Static list of authors with birth dates
- Displays dynamic Jinja templating

### Quotes Page
- Static inspirational reading quotes

### Team Page
- Simple team page using Jinja loops

### Testing
- End-to-end browser testing using Playwright
- Database seeding before tests
- Form interaction testing
- UI assertion testing

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
│   ├── test_app.py
│   ├── test_landing_page.py
│
├── book_store_venv/
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

Books table

```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT
);
```

Films table

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
Clears books table
Inserts test books

```sql
TRUNCATE TABLE books RESTART IDENTITY;

INSERT INTO books (title, author)
VALUES ('The Gruffalo', 'Julia Donaldson');
```

films.sql
Clears films table
Inserts test films

```sql
TRUNCATE TABLE films;

INSERT INTO films (title, director)
VALUES ('Mortal Kombat II', 'Simon McQuoid');
```

#### Environment Configuration

The app supports switching databases using environment variables:

DATABASE_NAME=book_store python app.py

Default:

book_store_test

Configured in:

lib/database_connection.py

#### Running Tests

Run all tests:

pytest

#### Make sure:

Flask server is running
Test database exists
Seed files are correct

#### Playwright Testing

Tests simulate real user behaviour:

Example:
Navigate to /books
Fill form fields
Submit form
Verify UI updates

page.get_by_placeholder("Title").fill("Harry Potter")
page.get_by_role("button", name="Submit").click()

#### Running the App

Start server:

python app.py

Then open:

http://127.0.0.1:5001/

#### Docker Setup

Build image:

docker build -t book-store-app .

Run container:

docker run -p 5001:5001 book-store-app


### requirements.txt

Key dependencies:

Flask
psycopg
pytest
playwright

(Full list included in repo)

## Key Learning Outcomes:
Flask routing (GET + POST)
HTML form handling
Jinja templating
PostgreSQL CRUD operations
Repository pattern (clean architecture)
Test-driven development (TDD)
End-to-end testing with Playwright
Database seeding for test isolation
Docker containerisation

## Test Strategy:
Unit-style DB setup via seed files
Full browser tests with Playwright
Independent test database (book_store_test)
Clean reset before each test run

Built as part of a full-stack Python training project using Flask, PostgreSQL, and Playwright testing.