from datetime import date
import re
from flask_wtf import FlaskForm
from wtforms import(
    StringField, PasswordField,
    validators, DateField,
    TelField, ValidationError,
    EmailField
)
from flask_login import current_user
from src.models.user_model import UserManager, check_email, check_username


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", [validators.DataRequired(), validators.Length(min=4, max=99)])
    first_name = StringField("First Name", [validators.Length(min=2, max=40)])
    last_name = StringField("Last Name", [validators.Length(min=2, max=40)])
    email = EmailField("Email Address",
                       [validators.Length(min=10, max=40),
                        validators.Email(
                            message="This is not a valid email address."),
                           validators.DataRequired()])
    password = PasswordField("New Password",
                             [validators.DataRequired(),
                              validators.Length(min=8),
                              validators.EqualTo("confirm_password",
                                                 message="Passwords don't match.")
                              ]
                             )
    confirm_password = PasswordField(
        "Repeat Password", [validators.DataRequired()])
    birthday = DateField("Date of Birth", [validators.InputRequired(
        message="Your Date of Birth is required.")], format="%Y-%m-%d")
    phone_number = TelField("Phone Number")
    street_address = StringField("Street Address")
    province = StringField("Province")
    postal_code = StringField("Zip Code")
    country = StringField("Country")
    city = StringField("City")

    def validate_email(self, email):
        email_exists = check_email(email.data)
        if email_exists:
            raise ValidationError("This email address is already in use.")

    def validate_username(self, username):
        if (username.data or username.data.lower()) is ("admin" or "administration"):
            raise ValidationError("Username isn't acceptable.")
        username_exists = check_username(username.data)
        if username_exists:
            raise ValidationError("This username is already taken.")

    def validate_password(self, password):
        if re.fullmatch(r"^(?=.*[A-Öa-ö])(?=.*\d)(?=.*[@$!%*#?&])[A-Öa-ö\d@$!%*#?&]{1,}$",
                        password.data) is None:
            raise ValidationError(
                """Your password should contain at
                least one letter, one number,
                one special character.""")

    def validate_first_name(self, first_name):
        if re.fullmatch(r"^(\s)*[A-Öa-ö]+((\s)?((\'|\-|\.)?([A-Öa-ö])+))*(\s)*$",
                        first_name.data) is None:
            raise ValidationError("Please insert a first name.")

    def validate_last_name(self, last_name):
        if re.fullmatch(r"^(\s)*[A-Öa-ö]+((\s)?((\'|\-|\.)?([A-Öa-ö])+))*(\s)*$",
                        last_name.data) is None:
            raise ValidationError("Please insert a last name.")

    def validate_birthday(self, birth_date):
        age = date.today().year - birth_date.data.year
        if age <= 12:
            raise ValidationError(
                "Children's Online Privacy Protection Act limits the age of users to be over 13.")


class ProfileForm(FlaskForm):
    first_name = StringField("First Name", [validators.Length(min=2, max=40)])
    last_name = StringField("Last Name", [validators.Length(min=2, max=40)])
    email = EmailField("Email Address",
                       [validators.Length(min=10, max=40),
                        validators.Email(
                            message="This is not a valid email address."),
                           validators.DataRequired()])
    phone_number = TelField("Phone Number")
    street_address = StringField("Street Address")
    province = StringField("Province")
    postal_code = StringField("Zip Code")
    country = StringField("Country")
    city = StringField("City")

    def validate_email(self, email):
        current_email = UserManager(current_user.username).fetch_email()
        if current_email != email.data:
            email_exists = check_email(email.data)
            if email_exists:
                raise ValidationError("This email address is already in use.")
