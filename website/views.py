import re
from flask_login import current_user, login_required, login_user, logout_user
from flask import Blueprint, render_template, redirect, flash, url_for
from werkzeug.security import generate_password_hash
from uuid import uuid4
from flask import Flask, request
from dotenv import load_dotenv
from os import environ
from datetime import timedelta
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv("/home/koxhr/0000 Repositories/marketplace_tsoha/.env")
app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY") ## Insert a new secret key
app.config["UPLOAD_FOLDER"] = environ.get("UPLOAD_FOLDER")
app.config["SQLALCHEMY_DATABASE_URI"]= environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[" TEMPLATES_AUTO_RELOAD"] = True
app.permanent_session_lifetime = timedelta(hours=2)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'
csrf = CSRFProtect(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
from entity import User

views = Blueprint("views", __name__)
@views.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.fetch_user(form.email.data.lower())
        if user is None:
            flash("Email or password is incorrect.")
            return redirect(url_for("views.login"))
        login_user(user, remember=True)
        User.create_session(user)
        return redirect(url_for("views.home"))
    return render_template("/login.html", form=form)

@views.route("/logout")
@login_required
def logout():
    User.delete_session(current_user)
    logout_user()
    flash("You have logged out.", category="success")
    return redirect(url_for("views.login"))

from authentication_models import RegistrationForm, LoginForm
@views.route("/signup", methods=["GET", "POST"])
@views.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash=generate_password_hash(form.password.data)
        user = User(
            user_id=uuid4(),
            email=form.email.data.lower(),
            password=hash,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        User.create_session(user)
        user.create_user(
            street_address=form.street_address.data,
            phone_number=form.phone_number.data,
            city=form.city.data,
            state_prov=form.state_prov.data,
            postal_code=form.postal_code.data,
            birth_date=form.birth_date.data
        )
        login_user(user, remember=True)
        flash("Congratulations, your registration is complete.", category="success")
        return redirect(url_for("views.home"))
    return render_template("/register.html", form=form)

@views.route("/")
@views.route("/home")
def home():
    if current_user.is_anonymous:
        return render_template("index.html")
    return render_template("index.html", name=current_user.first_name)

@views.route("/marketplace")
@views.route("/market")
@login_required
def marketplace():
    return render_template("marketplace.html", items="Phone")

@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404
    
@app.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login to see this page.")
    return redirect(url_for('views.login'))