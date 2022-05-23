from flask import Blueprint, render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash

authentication = Blueprint("authentication", __name__)

@authentication.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = "blank for now, fetch from db"
    check_password_hash(hash_value, password)
    ## Tarkista käyttäjänimi & salasana

    session["username"] = username
    return "<p>Login</p>"


@authentication.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@authentication.route("/register")
def register():
    username = ""
    password = "blank for now"
    hash_value = generate_password_hash(password)
    check_password_hash(hash_value, password)
    return render_template("register.html", title="Register")