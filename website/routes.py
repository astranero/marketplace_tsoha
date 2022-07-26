import dotenv
from flask_login import current_user, login_required, login_user, logout_user
from flask import Blueprint, render_template, redirect, flash, url_for
from werkzeug.security import generate_password_hash
from uuid import uuid4
from flask import Flask, request
from dotenv import load_dotenv
from os import environ, remove, path
from datetime import timedelta
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename

load_dotenv("/home/koxhr/0000 Repositories/marketplace_tsoha/.env")
app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY") ## Insert a new secret key
app.config["UPLOAD_FOLDER"] = environ.get("UPLOAD_FOLDER")
app.config["SQLALCHEMY_DATABASE_URI"]= environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[" TEMPLATES_AUTO_RELOAD"] = True
app.permanent_session_lifetime = timedelta(hours=24)
login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'
db = SQLAlchemy(app)
login_manager.init_app(app)
csrf = CSRFProtect(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
from user_entity import User

views = Blueprint("views", __name__)
@views.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.fetch_user(form.username.data)
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

from authentication_models import ContactForm, PasswordChangeForm, RegistrationForm, LoginForm, ContactForm, ProfileForm
@views.route("/signup", methods=["GET", "POST"])
@views.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash=generate_password_hash(form.password.data)
        user = User(
            user_id=uuid4(),
            username=form.username.data,
            password=hash,
            first_name=form.first_name.data,
            )
        response = user.create_user(
            email=form.email.data,
            last_name=form.last_name.data,
            street_address=form.street_address.data,
            phone_number=form.phone_number.data,
            country=form.country.data,
            city=form.city.data,
            province=form.province.data,
            postal_code=form.postal_code.data,
            birthday=form.birthday.data
        )
        if response:
            User.create_session(user)
            login_user(user, remember=True)
            flash("Congratulations, your registration is complete.", category="success")
            return redirect(url_for("views.home"))
        else:
            flash("Something went wrong with registration, please try again.")
    return render_template("/register.html", form=form)

@app.context_processor
def post_injection():
    return dict(post_form=ContactForm(), profile_form=ProfileForm(), password_change_form=PasswordChangeForm())

@views.route("/", methods=["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
def home():
    if current_user.is_anonymous:
        return render_template("index.html")
    return render_template("index.html", name=current_user.first_name)

@views.route("/marketplace", methods=["GET", "POST"])
@views.route("/market", methods=["GET", "POST"])
@login_required
def marketplace():
    data = db.session.execute("SELECT * FROM products;").fetchall()
    return render_template("marketplace.html", products=data)

@views.route("/profile/<username>", methods=["POST", "GET"])
@login_required
def profile(username):
    return render_template("profile.html", username=username)

@views.route("/profile/edit/<username>", methods=["POST", "GET"])
@login_required
def profile_edit(username):
    if username == current_user.username:
        if "current_password" not in request.form:
            username = current_user.username
            form = ProfileForm()
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            phone_number = form.phone_number.data
            street_address = form.street_address.data
            country = form.country.data
            province = form.province.data
            postal_code = form.postal_code.data
            city = form.city.data
            if form.validate_on_submit():
                if first_name:
                    User.update_first_name(username, first_name)
                if last_name:
                    User.update_last_name(username, last_name)
                if email:
                    User.update_email(username, email)
                if phone_number:
                    User.update_phone_number(username, phone_number)
                if street_address:
                    User.update_street_address(username, street_address)
                if country:
                    User.update_country(username, country)
                if province:
                    User.update_province(username, province)
                if postal_code:
                    User.update_postal_code(username, postal_code)
                if city:
                    User.update_city(username, city)
                flash("Your profile has been updated.")
            return render_template("profile/edit.html", username=current_user.username, profile_form=form)

        elif "current_password" in request.form:
            form = PasswordChangeForm()
            if form.validate_on_submit():
                hash=generate_password_hash(form.new_password.data)
                User.update_password(current_user.username, hash)
                flash("Your password has been changed.")
            return render_template("profile/edit.html", username=current_user.username, password_change_form=form)

    flash("You can't edit other user's profile.")
    return redirect(url_for("views.home"))

@views.route("/product/<int:product_id>", methods=["POST","GET"])
@login_required
def product(product_id):
    return render_template("product.html", product_id=product_id)

@views.route("/product/edit/<int:product_id>", methods=["POST","GET"])
@login_required
def product_edit(product_id):
    pass

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/contact", methods=["POST"])
def contact():
    contact_data = ContactForm()
    if contact_data.validate_on_submit:
        contact_data.send_contact_us_message(contact_data.email.data, contact_data.message.data)
        flash("Your message has been sent.")
    return redirect(url_for("views.home"))

@views.route("/product/<int:product_id>/comment", methods=["POST"])
@login_required
def comment(product_id):
    if request.method=="POST":
        if "comment" in request.form():
            product_add_comment()
        return redirect(url_for("views.product", product_id=product_id))
    return redirect(url_for("views.marketplace"))



ALLOWED_PROFILE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PROFILE_EXTENSIONS

@views.route("/uploader")
@login_required
def new_uploader():
    return redirect(url_for("views.profile", username=current_user.username))

@views.route("/uploader", methods=["POST"])
@login_required
def picture_uploader():
    if request.method == "POST" :
        if "profile_picture" in request.files:
            profile_picture = User.fetch_profile_picture(current_user.username)
            file = request.files.get("profile_picture")
            if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = str(uuid4())
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                file.filename = filename+"."+file_extension
                secured_filename = secure_filename(file.filename)
                file.save(path.join(app.root_path, "static/images/"+secured_filename))
                User.update_profile_picture(current_user, current_user.username, secured_filename)
                flash("Profile picture has been uploaded.")
                if profile_picture != "default.jpg":
                    remove(path.join(app.root_path, "static/images/"+profile_picture))
                    
            else:
                flash("Acceptable extensions are: png, jpg, jpeg and gif.")
    return redirect(request.url)

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