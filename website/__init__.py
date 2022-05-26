from os import getenv, path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2


app = Flask(__name__)
db = SQLAlchemy(app)
conn = False

def create_app():
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["UPLOAD_FOLDER"] = getenv("UPLOAD_FOLDER")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{getenv('DB_NAME')}"
  
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app

"""def connection():
    global conn
    if not conn:
        conn = psycopg2.connect(f"{getenv('DB_NAME')} {getenv('DB_USER')}")
    return conn"""
'''
def create_db():
    if not path.exists("website/"+getenv('DB_NAME')):
        db.create_all(app=app)'''