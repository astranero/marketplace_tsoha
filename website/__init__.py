from os import getenv, path
from dotenv import load_dotenv
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import psycopg2, os


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = getenv("UPLOAD_FOLDER")
app.config["SQLALCHEMY_DATABASE_URI"]=getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=2)
db = SQLAlchemy(app)

def create_app():
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app
