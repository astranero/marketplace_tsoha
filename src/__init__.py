from os import environ
from datetime import timedelta
from flask_login import LoginManager
from flask import Flask

from dotenv import load_dotenv
load_dotenv("/home/koxhr/0000 Repositories/marketplace_tsoha/.env")
app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = environ.get("UPLOAD_FOLDER")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[" TEMPLATES_AUTO_RELOAD"] = True
app.permanent_session_lifetime = timedelta(hours=24)
login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'
