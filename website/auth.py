from turtle import pos
from flask import Flask, Blueprint, render_template, request, session, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from website.forms import RegistrationForm
from repositories.user_management import create_user


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
        if "username" in session: 
            return redirect(url_for("auth.user"))
        
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
    flash("Olet kirjautunut ulos!")
    return redirect("login")

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        street_address = form.street_address.data
        phone_number = form.phone_number.data
        city = form.city.data
        state_prov = form.state_prov.data
        postal_code = form.postal_code.data
        birth_date = form.birth_date.data
        create_user(email, first_name, last_name,password, street_address, phone_number, city, state_prov, postal_code,
        birth_date)
        
        session["username"] = form.username.data
        flash("Registration complete!")
        return redirect(url_for("auth.user"))
    return render_template("/register.html", form=form)

@auth.before_app_request
def load_logged_in_user():
    username = session.get("username")
    pass
