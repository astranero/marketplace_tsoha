from datetime import date
import re
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField,
    validators, DateField,
    TelField, ValidationError,
    EmailField, TextAreaField
)
from user_entity import User, check_email, check_username
from flask_login import current_user
from werkzeug.security import check_password_hash
from markupsafe import Markup
from message_manager import MessageManager


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
        if re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{1,}$",
                        password.data) is None:
            raise ValidationError(
                """Your password should contain at
                least one letter, one number,
                one special character.""")

    def validate_first_name(self, first_name):
        if re.fullmatch(r"^(\s)*[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*(\s)*$",
                        first_name.data) is None:
            raise ValidationError("Please insert a first name.")

    def validate_last_name(self, last_name):
        if re.fullmatch(r"^(\s)*[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*(\s)*$",
                        last_name.data) is None:
            raise ValidationError("Please insert a last name.")

    def validate_birthday(self, birth_date):
        age = date.today().year - birth_date.data.year
        if age <= 12:
            raise ValidationError(
                "Children's Online Privacy Protection Act limits the age of users to be over 13.")


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
        current_email = current_user.fetch_email(current_user.username)
        if current_email != email.data:
            email_exists = check_email(email.data)
            if email_exists:
                raise ValidationError("This email address is already in use.")


class ContactForm(FlaskForm):
    email = StringField("Email",
                        [validators.Length(min=4, max=40),
                         validators.Email(
                             message="Email address format is incorrect."),
                         validators.DataRequired()])
    message = TextAreaField("message", [validators.Length(
        min=4)])

    def send_message(self, sender, message):
        message = MessageManager(sender, message, tag="contact-us")
        message.insert_message()


class MessageForm(FlaskForm):
    sender = StringField("sender", [validators.Length(
        min=4, max=40),
        validators.Email(message="Username format is incorrect."),
        validators.DataRequired()])
    receiver = StringField("receiver", [
        validators.Length(min=4, max=40),
        validators.Email(message="Username format is incorrect."),
        validators.DataRequired()])
    message = TextAreaField("message",
                            [validators.Length(min=0),
                             validators.DataRequired()])

    def validate_receiver(self, receiver):
        username_exists = check_username(receiver)
        if not username_exists:
            raise ValidationError(
                Markup("Username doesn't exist"))

    def validate_sender(self, sender):
        username = current_user.username
        if sender == username:
            raise ValidationError("You can't send message to yourself.")

    def send_message(self, sender, receiver, message):
        message = MessageManager(sender, message, receiver)
        message.insert_message()

    def send_report(self, sender, message):
        message = MessageManager(sender, message, tag="report")
        message.insert_message()


class CommentReportForm(FlaskForm):
    sender = StringField("sender", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    reported = StringField("reported", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    product_id = StringField("product_id", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    comment_id = StringField("comment_id", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    comment = StringField("comment", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    message = TextAreaField("message", [validators.Length(
        min=0), validators.DataRequired()])

    def validate_reported(self, reported):
        username_exists = check_username(reported)
        if not username_exists:
            raise ValidationError(
                Markup("Username doesn't exist"))

    def validate_sender(self, sender):
        username = current_user.username
        if sender == username:
            raise ValidationError("You can't send message to yourself.")

    def send_report(self, sender, message):
        message = MessageManager(sender, message, tag="report")
        message.insert_message()
