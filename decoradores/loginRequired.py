from flask import session, flash, redirect, url_for
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            flash("Inicia sesión para continuar")
            return redirect(url_for("login.home"))
        return view_func(*args, **kwargs)
    return wrapped_view
