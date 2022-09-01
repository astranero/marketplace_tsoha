import json
from uuid import uuid4
from os import remove, path
import click
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, redirect, flash, url_for, request, abort
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from src.__init__ import app, login_manager
from src.forms.messaging_form import (
    MessageForm,
    CommentReportForm
)
from src.forms.login_form import LoginForm
from src.forms.registration_form import (RegistrationForm, ProfileForm)
from src.models.user_model import(
    UserManager,
    ProfileManager,
    User,
    check_username
)
from src.models.product_models import(
    FilterManager,
    ProductManager,
    check_product_exists,
    delete_product,
    delete_product_images,
    fetch_issold,
    fetch_product_imgs,
    fetch_product_img,
    fetch_product,
    fetch_bought_products,
    fetch_sold_products,
    fetch_user_products,
    update_issold,
    count_sold_products
)
from src.models.messaging_models import CommentManager, MessageManager, count_messages
from src.forms.password_change_form import PasswordChangeForm
db = SQLAlchemy(app)
login_manager.init_app(app)
csrf = CSRFProtect(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    password_hash = generate_password_hash(password)
    user = UserManager(username=username)
    registration_info = {
        "username": None,
        "password": password_hash,
        "first_name": None,
        "email": str(uuid4())+"@admin.admin",
        "last_name": None,
        "street_address": None,
        "phone_number": 000000000,
        "country": None,
        "city": None,
        "province": None,
        "postal_code": None,
        "birthday": None,
        "profile_picture_id": "default.png"
    }
    user.create_user(registration_info)
    user.update_is_admin(True)


ALLOWED_PROFILE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PROFILE_EXTENSIONS


filter_manager = FilterManager()
views = Blueprint("views", __name__)


@login_manager.user_loader
def user_loader(user_id):
    return User.get(current_user, user_id=user_id)


@views.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    form = LoginForm()

    if form.validate_on_submit():

        user = UserManager(username=form.username.data).fetch_user()
        login_user(user, remember=True)
        user.create_session(user)
        if not current_user.is_active:
            flash("You can't access this page since you have been banned.")
        return redirect(url_for("views.home"))
    return render_template("/login.html", form=form)


@views.route("/logout")
@login_required
def logout():
    current_user.delete_session()
    logout_user()
    flash("You have logged out.", category="success")
    return redirect(url_for("views.login"))


@views.route("/signup", methods=["GET", "POST"])
@views.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user = UserManager(username=form.username.data)
        registration_info = {
            "username": form.username.data,
            "password": password_hash,
            "first_name": form.first_name.data,
            "email": form.email.data,
            "last_name": form.last_name.data,
            "street_address": form.street_address.data,
            "phone_number": form.phone_number.data,
            "country": form.country.data,
            "city": form.city.data,
            "province": form.province.data,
            "postal_code": form.postal_code.data,
            "birthday": form.birthday.data,
            "profile_picture_id": "default.png",
            "admin": False
        }
        user = user.create_user(registration_info)
        if user:
            user.create_session(user)
            login_user(user, remember=True)
            flash("Congratulations, your registration is complete.",
                  category="success")
            return redirect(url_for("views.home"))
        flash("Something went wrong with registration, please try again.")
    return render_template("/register.html", form=form)


@app.context_processor
def post_injection():
    return dict(
        message_form=MessageForm(),
        profile_form=ProfileForm(),
        password_change_form=PasswordChangeForm(),
        report_form=CommentReportForm(),
        message_manager=MessageManager,
        profile_manager=ProfileManager(),
        user_manager=UserManager,
        filter_manager=FilterManager(),
        get_profile_picture=ProfileManager().get_profile_picture,
        fetch_issold=fetch_issold,
        fetch_product_imgs=fetch_product_imgs,
        fetch_product_img=fetch_product_img,
        fetch_product=fetch_product,
        fetch_profile_picture=ProfileManager().fetch_profile_picture,
        check_product_exists=check_product_exists,
        fetch_bought_products=fetch_bought_products,
        fetch_sold_products=fetch_sold_products,
        fetch_user_products=fetch_user_products,
        count_sold_products=count_sold_products,
        count_messages=count_messages
    )


@views.route("/", methods=["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
def home():
    if current_user.is_anonymous:
        return render_template("index.html")
    return render_template("index.html", name=current_user.first_name)


@views.route("/marketplace", methods=["GET"])
@views.route("/market", methods=["GET"])
@login_required
def marketplace():
    products = filter_manager.fetch_products()
    return render_template("marketplace.html", products=products)


@views.route("/set_condition/<condition>")
@login_required
def set_condition(condition):
    filter_manager.set_condition(condition)
    return redirect(url_for("views.marketplace"))


@views.route("/set_category/<category>")
@login_required
def set_category(category):
    filter_manager.set_category(category)
    return redirect(url_for("views.marketplace"))


@views.route("/set_sort/<sort>")
@login_required
def set_sort(sort):
    filter_manager.set_sort(sort)
    return redirect(url_for("views.marketplace"))


@views.route("/set_search")
@login_required
def set_search():
    search = request.args["search"]
    filter_manager.set_search(search)
    return redirect(url_for("views.marketplace"))


@views.route("/marketplace", methods=["POST"])
@views.route("/market", methods=["POST"])
@login_required
def product_add():
    if request.method == "POST":
        data = request.files.getlist("product_pictures")
        product_info = {"title": request.form["title"],
                        "details": request.form["details"],
                        "price": request.form["price"],
                        "category": request.form["category"],
                        "condition": request.form["condition"]}
        product_id = str(uuid4())
        new_product = ProductManager(product_id=product_id,
                                     username=current_user.username)
        new_product.set_product_info(product_info=product_info)
        new_product.insert_product()
        for file in data:
            if file and allowed_file(file.filename):
                filename = str(uuid4())
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                file.filename = filename+"."+file_extension
                secured_filename = secure_filename(file.filename)
                file.save(path.join(app.root_path+
                          "/static/images/"+secured_filename))
                new_product.insert_product_imgs(img_id=secured_filename)
            else:
                flash("Acceptable extensions are: png, jpg, jpeg and gif.")
                return redirect(request.url)
    return redirect(url_for("views.marketplace"))


@views.route("/product/<product_id>", methods=["GET"])
@login_required
def product(product_id):
    comments = CommentManager(product_id=product_id).fetch_comments()
    return render_template("product.html",
                           product_id=product_id,
                           comments=comments)


@views.route("/product_delete/<product_id>", methods=["GET"])
@login_required
def product_delete(product_id):
    imgs = fetch_product_imgs(product_id)
    if imgs is not None:
        for img in imgs:
            if path.exists(app.root_path+"/static/images/"+img[0]):
                remove(path.join(app.root_path+"/static/images/"+img[0]))
    delete_product(product_id)
    return redirect(url_for("views.marketplace"))


@views.route("/product/<product_id>/<comment_id>", methods=["GET"])
@login_required
def comment_delete(product_id, comment_id):
    CommentManager(comment_id=comment_id).delete_comment()
    comments = CommentManager(product_id=product_id).fetch_comments()
    return render_template("product.html",
                           product_id=product_id,
                           comments=comments
                           )


@views.route("/product/<product_id>/comment", methods=["POST"])
@login_required
def comment(product_id):
    if request.method == "POST":
        new_comment = request.form["comment"]
        mgr = CommentManager(
            comment=new_comment,
            product_id=product_id,
            username=current_user.username
        )
        mgr.insert_comments()
        comments = CommentManager(product_id=product_id).fetch_comments()
        return redirect(url_for("views.product",
                                product_id=product_id,
                                comments=comments))
    return redirect(url_for("views.marketplace"))


@views.route("/product_edit/<product_id>", methods=["POST"])
@login_required
def product_edit(product_id):
    if request.method == "POST":
        product_info = {"title": request.form["title"],
                        "details": request.form["details"],
                        "price": request.form["price"],
                        "category": request.form["category"],
                        "condition": request.form["condition"]}
        product_mgr = ProductManager(
            username=current_user.username,
            product_id=product_id)
        images = request.files.getlist("product_pictures")
        if images:
            delete_product_images(product_id)
            for file in images:
                if file and allowed_file(file.filename):
                    filename = str(uuid4())
                    file_extension = file.filename.rsplit('.', 1)[1].lower()
                    file.filename = filename+"."+file_extension
                    secured_filename = secure_filename(file.filename)
                    file.save(path.join(app.root_path+
                              "/static/images/"+secured_filename))
                    product_mgr.insert_product_imgs(img_id=secured_filename)
                else:
                    flash("Acceptable extensions are: png, jpg, jpeg and gif.")
        product_mgr.set_product_info(product_info=product_info)
        product_mgr.update_title()
        product_mgr.update_details()
        product_mgr.update_price()
        product_mgr.update_category()
        product_mgr.update_condition()
        flash("Your product has been updated.")
    return redirect(url_for("views.product", product_id=product_id))


@views.route("/buy_product/<product_id>")
@login_required
def buy_product(product_id):
    issold = fetch_issold(product_id)
    if not issold:
        update_issold(is_sold=True, sold_to=current_user.username,
                      product_id=product_id)
        flash("You have bought this product succesfully.")
    else:
        flash("This product has already been sold.")
    return redirect(url_for("views.product", product_id=product_id))


@views.route("/return_product/<product_id>")
@login_required
def return_product(product_id):
    update_issold(is_sold=False, sold_to=None, product_id=product_id)
    flash("Product has been returned succesfully.")
    return redirect(url_for("views.profile", username=current_user.username))


@views.route("/profile/<username>", methods=["GET"])
@login_required
def profile(username):
    if check_username(username):
        return render_template("profile.html", username=username)
    return render_template("404.html")


@views.route("/profile_edit/<username>", methods=["POST", "GET"])
@login_required
def profile_edit(username):
    if username == current_user.username:
        mgr = UserManager(username=username)
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
                mgr.update_first_name(first_name)
                mgr.update_last_name(last_name)
                mgr.update_email(email)
                mgr.update_phone_number(phone_number)
                mgr.update_street_address(
                    street_address)
                mgr.update_country(country)
                mgr.update_province(province)
                mgr.update_postal_code(postal_code)
                mgr.update_city(city)
                flash("Your profile has been updated.")
            return render_template(
                "profile_edit.html",
                username=current_user.username,
                profile_form=form)

        if "current_password" in request.form:
            form = PasswordChangeForm()
            if form.validate_on_submit():
                hashed_password = generate_password_hash(
                    form.new_password.data)
                mgr.update_password(hashed_password)
                flash("Your password has been changed.")
            return render_template(
                "profile_edit.html",
                username=current_user.username,
                password_change_form=form
            )
    flash("You can't edit other user's profile.")
    return redirect(url_for("views.home"))


@views.route("/delete_profile")
@login_required
def delete_profile():
    products = fetch_user_products(current_user.username)
    for item in products:
        imgs = fetch_product_imgs(item.id)
        if imgs is not None:
            for img in imgs:
                if path.exists(app.root_path+"/static/images/"+img[0]):
                    remove(path.join(app.root_path+"/static/images/"+img[0]))
    ProfileManager().delete_profile(current_user.username)
    current_user.delete_session()
    logout_user()
    flash("Profile succesfully deleted.", category="success")
    return redirect(url_for("views.login"))


@views.route("/about")
def about():
    return render_template("about.html")


@login_required
@views.route("/send_message", methods=["POST", "GET"])
def send_message():
    message_data = MessageForm()
    if message_data.validate_on_submit:
        if not check_username(message_data.receiver.data):
            flash("This user does not exist.")
            return redirect(url_for("views.home"))
        if not message_data.send_message(
                sender=message_data.sender.data,
                message=message_data.message.data,
                receiver=message_data.receiver.data):
            flash("You can't message yourself.")
            redirect(url_for("views.messages", username=current_user.username))
        else:
            flash("Your message has been sent.")
    return redirect(url_for("views.messages", username=current_user.username))


@login_required
@views.route("/report/<product_id>", methods=["POST"])
def report(product_id):
    message_data = CommentReportForm()
    if message_data.validate_on_submit:
        sender = message_data.sender.data
        reported = message_data.reported.data
        new_message = message_data.message.data
        reported_comment = message_data.comment.data
        comment_id = message_data.comment_id.data
        product_id = message_data.product_id.data

        json_packet = {"product_id": product_id,
                       "comment_id": comment_id,
                       "sender": sender,
                       "reported": reported,
                       "commented": reported_comment,
                       "new_message": new_message
                       }
        json_data = json.dumps(json_packet)
        message_data.send_report(sender, json_data)
        flash("Report has been sent.")
    return redirect(url_for("views.product", product_id=product_id))


@login_required
@views.route("/profile/<username>/messages", methods=["POST", "GET"])
def messages(username):
    if username == current_user.username:
        data = MessageManager(receiver=username).fetch_senders()
        if not data:
            data = MessageManager(sender=username).fetch_receivers()
        return render_template("messages.html", username=username, data=data)
    return redirect(url_for("views.profile", username=username))


@login_required
@views.route("/like/<username>", methods=["POST", "GET"])
def like(username):
    profile_mgr = ProfileManager()
    exists = profile_mgr.has_liked_profile(current_user.username, username)
    islike = profile_mgr.fetch_profile_islike(current_user.username, username)
    if exists and not islike:
        profile_mgr.update_profile_like(
            current_user.username,
            username,
            True
        )
    if not exists:
        profile_mgr.like_profile(
            current_user.username,
            username,
            True
        )
    return redirect(url_for("views.profile", username=username))


@login_required
@views.route("/dislike/<username>", methods=["POST", "GET"])
def dislike(username):
    profile_mgr = ProfileManager()
    profile_mgr.update_profile_like(
        current_user.username,
        username,
        islike=False
    )
    return redirect(url_for("views.profile", username=username))


@login_required
@views.route("/profile/<username>/messages/delete_all_messages/<sender>", methods=["GET"])
def delete_all_messages(username, sender):
    if current_user.username == username:
        MessageManager(
            sender=sender, receiver=current_user.username).delete_messages()
        MessageManager(sender=current_user.username,
                       receiver=sender).delete_messages()
    return redirect(url_for("views.messages", username=current_user.username))


@login_required
@views.route("/profile/<username>/messages/delete_message/<message_id>", methods=["GET"])
def delete_message(username, message_id):
    if current_user.username == username:
        MessageManager(message_id=message_id).delete_message()
    return redirect(url_for("views.messages", username=current_user.username))


@login_required
@views.route("hide_report/<message_id>")
def hide_report(message_id):
    if current_user.is_admin:
        MessageManager(message_id=message_id).update_tag("solved")
    return redirect(url_for("views.admin"))


@views.route("/uploader", methods=["POST"])
@login_required
def picture_uploader():
    profile_mgr = ProfileManager()
    if request.method == "POST":
        if "profile_picture" in request.files:
            profile_picture = profile_mgr.fetch_profile_picture(
                current_user.username)
            file = request.files.get("profile_picture")
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = str(uuid4())
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                file.filename = filename+"."+file_extension
                secured_filename = secure_filename(file.filename)
                file.save(
                    path.join(
                        app.root_path+"/static/images/"+secured_filename)
                )
                profile_mgr.update_profile_picture(
                    current_user.username,
                    secured_filename)
                flash("Profile picture has been uploaded.")
                try:
                    if profile_picture != "default.png":
                        remove(path.join(app.root_path+
                               "/static/images/"+profile_picture))
                except FileNotFoundError:
                    pass
            else:
                flash("Acceptable extensions are: png, jpg, jpeg and gif.")
    return redirect(url_for("views.profile_edit", username=current_user.username))


@views.route("/admin", methods=["GET"])
@login_required
def admin():
    if current_user.is_admin:
        fetched_messages = MessageManager().fetch_report_messages()
        datas = []
        for message in fetched_messages:
            data = {}
            data["id"] = message[0]
            data["sender"] = message[1]
            try:
                data["message"] = json.loads(message[3])
            except json.JSONDecodeError:
                pass
            data["creation_date"] = message[4]
            datas.append(data)
        return render_template("admin.html", messages=datas)
    return abort(404)


@login_required
@views.route("/ban/<username>")
def ban(username):
    UserManager(username=username).update_activity(False)
    return redirect(url_for("views.admin"))


@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login to see this page.")
    return redirect(url_for('views.login'))
