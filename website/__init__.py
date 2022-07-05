from os import getenv, path
from dotenv import load_dotenv
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import psycopg2


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = getenv("UPLOAD_FOLDER")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{getenv('DB_NAME')}"
app.permanent_session_lifetime = timedelta(hours=2)
db = SQLAlchemy

def create_app():
    from .views import views
    from .auth import auth
    db(app)
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app


def return_app():
    return app


conn = False
"""def connection():
    global conn
    if not conn:
        conn = psycopg2.connect(f"{getenv('DB_NAME')} {getenv('DB_USER')}")
    return conn"""
'''
def create_db():
    if not path.exists("website/"+getenv('DB_NAME')):
        db.create_all(app=app)'''
