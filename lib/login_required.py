from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If the user doesn't have a valid session ID, kick them out to the login form
        if "user_id" not in session:
            return redirect("/sessions/new")
        # Otherwise, let them proceed to the original route function!
        return f(*args, **kwargs)
    return decorated_function