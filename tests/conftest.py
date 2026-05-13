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
        ["flask", "run", "--no-reload", "--port=5001"],
        env={ # running in testing mode, keeping all normal system variables
            **os.environ,
            "FLASK_ENV": "test",
            "FLASK_APP": "app.py"
        },
        stdout=subprocess.PIPE, # Capturing output, without printing Flask logs into terminal
        stderr=subprocess.PIPE
    )

    # wait for server to be ready
    # request books
    # if it works, server is ready
    # if it fails, wait 0.5 seconds and try again
    for _ in range(30):
        try:
            r = requests.get("http://127.0.0.1:5001/books")
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.5)
    else:
        process.terminate()
        raise Exception("Flask did not start") # if server still not ready, terminate so we don't wait forever

    yield # splits function into 2 phases: before yield (start server) and after yield (teardown/cleanup)

    process.terminate() # stop Flask server
    process.wait() # wait until it fully shuts down