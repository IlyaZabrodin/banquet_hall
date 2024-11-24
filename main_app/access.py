from functools import wraps
from typing import Callable, List

from flask import session, redirect, url_for, abort


def login_required(allowed_roles: List[str] = []) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(allowed_roles) != 0 and (session['user_group'] not in allowed_roles):
                #print(session['user_group'])
                abort(redirect('/access_fail'))
            if 'user_id' in session:
                return func(*args, **kwargs)
            return redirect(url_for('bp_auth.start_auth'))

        return wrapper
    return decorator

