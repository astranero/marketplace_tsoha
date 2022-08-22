import re
from flask_wtf import FlaskForm
from wtforms import (PasswordField,
                     validators,
                     ValidationError
                     )
from flask_login import current_user
from werkzeug.security import check_password_hash


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField(
        "current_password", [validators.DataRequired()])
    new_password = PasswordField("New Password",
                                 [validators.DataRequired(),
                                  validators.Length(min=8),
                                  validators.EqualTo("confirm_new_password",
                                                     message="Passwords don't match."
                                                     )
                                  ]
                                 )
    confirm_new_password = PasswordField(
        "Repeat Password", [validators.DataRequired()])

    def validate_new_password(self, new_password):
        if re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{1,}$",
                        new_password.data) is None:
            raise ValidationError(
                """Your password should contain at
                least one letter, one number,
                one special character.""")

    def validate_current_password(self, current_password):
        hashed_password = current_user.get_password(current_user.username)
        if not check_password_hash(hashed_password, current_password.data):
            raise ValidationError("Your password is incorrect.")
