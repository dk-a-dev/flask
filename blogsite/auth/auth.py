import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from blogsite.database.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form['password']
        email=request.form['email']
        db=get_db()
        error=None

        if not username:
            error='Username is required'
        elif not password:
            error='Password is required'
        elif not email:
            error='Email is required'
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user(email,username,password) VALUES (?,?,?)",
                    (email,username,generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error=f"User:{username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)
    return render_template('auth/register.html')
