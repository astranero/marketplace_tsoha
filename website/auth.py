from turtle import pos
from flask import Flask, Blueprint, render_template, request, session, redirect, flash, url_for
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from website.__init__ import db

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
    flash("Olet kirjautunut ulos!")
    return redirect("login")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        repeat_password = request.form["repeat_password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        birth_date = request.form["date"]
        phone_number = request.form["tel"]
        street_address = request.form["street_address"]
        state_prov = request.form["state_prov"]
        postal_code = request.form["postal_code"]  
        city = request.form["city"] 

        hash_value = generate_password_hash(password)
        sql ='''INSERT INTO users (email, password, first_name, last_name,street_address,phone_number, city, state_prov, postal_code, birth_date)
        VALUES (:email, :hash_value, :first_name, :last_name, :street_address, :phone_number,
        :city, :state_prov, :postal_code, :birth_date)'''

        db.session.execute(sql, {"email":email, "hash_value":hash_value, 
        "first_name":first_name, "last_name":last_name, "street_address":street_address,
        "phone_number":phone_number, "city":city, "state_prov":state_prov, "postal_code":postal_code, "birth_date":birth_date})
        
        db.session.commit()
        error = None
        if not email:
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
