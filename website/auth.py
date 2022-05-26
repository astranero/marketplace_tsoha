from flask import Flask, Blueprint, render_template, request, session, redirect, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = "blank for now, fetch from db"
        if check_password_hash(hash_value, password): pass
    return render_template("/login.html", title="Login")
    ## Tarkista käyttäjänimi & salasana

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        error = None
        if not username: error = "Username is required!"
        elif not password: error = "Password is required!"

        
        check_password_hash(hash_value, password)
        flash(error)

    return render_template("/register.html", title="Register")


@auth.before_app_request
def load_logged_in_user():
    username = session.get("username")
    pass
    
