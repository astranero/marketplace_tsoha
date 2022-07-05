from flask import Flask, Blueprint, render_template, request, session, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = "blank for now, fetch from db"
        
        session["username"] = username
        if check_password_hash(hash_value, password):
            pass
        # Tarkista käyttäjänimi & salasana
        
        return redirect(url_for("auth.user"))
    else:
        if "username" in session: return redirect(url_for("auth.user"))
        return render_template("/login.html", title="Login")
    

@auth.route("/user")
def user():
    if "username" in session:
        username = session["username"]
        print(username)
    else: return redirect(url_for("auth.login"))

@auth.route("/logout")
def logout():
    session.clear()
    flash("Olet kirjautunut ulos!", "info")
    return redirect("login")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        error = None
        if not username:
            error = "Username is required!"
        elif not password:
            error = "Password is required!"

        check_password_hash(hash_value, password)
        flash(error)

    return render_template("/register.html", title="Register")

@auth.before_app_request
def load_logged_in_user():
    username = session.get("username")
    pass
