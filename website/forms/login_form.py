from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField,
    validators,ValidationError)
from models.user_model import User, check_username
from flask_login import current_user
from werkzeug.security import check_password_hash
from markupsafe import Markup

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(
        min=4, max=99), validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])

    def validate_username(self, username):
        username_exists = check_username(username.data)
        if not username_exists:
            raise ValidationError(
                Markup("<p> User is not registered. <a href=register> Register here</a></p>"))
        self.password_validation(self.password)

    def password_validation(self, password):
        hashed_password = User.get_password(current_user, self.username.data.lower())
        if not check_password_hash(hashed_password, password.data):
            raise ValidationError(
                "Your username or password is incorrect.")