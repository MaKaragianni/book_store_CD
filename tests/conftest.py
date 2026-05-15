import os
import subprocess
import pytest
import time
import requests


@pytest.fixture(scope="session", autouse=True) 
# "scope="session" to run server once
# "autouse=True" no need to call this fixture in tests, pytest runs it automatically
def flask_server(): # starting web server before tests begin
    process = subprocess.Popen(
        ["python", "-m", "flask", "run", "--no-reload", "--port=5001"],
        env={ # running in testing mode, keeping all normal system variables
            **os.environ,
            "FLASK_APP": "app.py",
            "FLASK_ENV": "test",
            "DATABASE_NAME": "book_store_test",
            "DATABASE_USER": "runner",
            "DATABASE_HOST": "127.0.0.1",
            "DATABASE_PORT": "5432"
        },
        stdout=subprocess.PIPE, # Capturing output, without printing Flask logs into terminal
        stderr=subprocess.PIPE,
        text=True
    )

    # wait for server to be ready
    # request books
    # if it works, server is ready
    # if it fails, wait 0.5 seconds and try again
    for _ in range(30):
        try:
            r = requests.get("http://127.0.0.1:5001/books")
            if r.status_code in [200, 302]:
                break
        except Exception:
            pass

        if process.poll() is not None:
            stdout, stderr = process.communicate()

            print("FLASK STDOUT:")
            print(stdout)

            print("FLASK STDERR:")
            print(stderr)

            raise Exception("Flask crashed during startup")

        time.sleep(0.5)

    else:
        process.terminate()

        stdout, stderr = process.communicate()

        print("FLASK STDOUT:")
        print(stdout)

        print("FLASK STDERR:")
        print(stderr)

        raise Exception("Flask did not start")

    yield # splits function into 2 phases: before yield (start server) and after yield (teardown/cleanup)

    process.terminate() # stop Flask server
    process.wait() # wait until it fully shuts down


# DATABASE CLEANUP FIXTURE
@pytest.fixture(autouse=True)
def clean_users_table():
    """
    Runs before EVERY test automatically.
    Keeps users table empty so tests don't conflict.
    """

    from lib.database_connection import DatabaseConnection

    DatabaseConnection.connect()
    connection = DatabaseConnection.get_connection()

    connection.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;") # wipes table, resets ID
    connection.commit()

    yield # pauses till all tests finish