from functools import wraps

from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('bp_auth.start_auth'))
    return wrapper
