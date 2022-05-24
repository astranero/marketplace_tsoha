from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["UPLOAD_FOLDER"] = getenv("UPLOAD_FOLDER")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db = SQLAlchemy(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app

conn = None
def get_db():
    if conn is None:
        conn = psycopg2.connect(dbname=getenv["DB_NAME"], user=getenv["DB_USER"], password=getenv["DB_PASS"], host=getenv["DB_HOST"])
    return conn