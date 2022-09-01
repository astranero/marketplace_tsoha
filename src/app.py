from src.views import app, views
from os import environ
from datetime import timedelta
from flask_login import LoginManager
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = environ.get("UPLOAD_FOLDER")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[" TEMPLATES_AUTO_RELOAD"] = True
app.permanent_session_lifetime = timedelta(hours=24)
login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run()