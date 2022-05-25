from flask import Blueprint, render_template

views = Blueprint("views", __name__)
marketplace = Blueprint("marketplace", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("index.html")


@marketplace.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")