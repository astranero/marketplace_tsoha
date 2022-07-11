import re
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, DateField, IntegerField, TelField, ValidationError, EmailField
from views import db
from werkzeug.security import check_password_hash


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", [validators.Length(min=2, max=40)])
    last_name = StringField("Last Name", [validators.Length(min=2, max=40)])
    email = StringField("Email Address", [validators.Length(
        min=10, max=40), validators.Email(message="This is not a valid email address."), validators.DataRequired()])
    password = PasswordField("New Password", [validators.DataRequired(), validators.Length(min=8),
                                              validators.EqualTo("sec_password", message="Passwords don't match.")])
    sec_password = PasswordField(
        "Repeat Password", [validators.DataRequired()])
    birth_date = DateField("Date of Birth", [validators.InputRequired(
        message="Your Date of Birth is required.")], format="%Y-%m-%d")
    phone_number = TelField("Your Phone Number")
    street_address = StringField("Street Address")
    state_prov = StringField("State/Province")
    postal_code = StringField("Postal/Zip Code")
    city = StringField("City")

    def validate_email(self, email):
        SQL = "SELECT EXISTS(SELECT email FROM users WHERE email=:email);"
        db_email = db.session.execute(SQL, {"email": email.data}).fetchone()[0]
        if db_email:
            raise ValidationError("This email address is already in use.")

    def validate_password(self, password):
        if re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{1,}$", password.data) is None:
            raise ValidationError(
                "Your password should contain at least one letter, one number, one special character.")

    def validate_first_name(self, first_name):
        if re.fullmatch(r"^(\s)*[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*(\s)*$", first_name.data) is None:
            raise ValidationError("Please insert a first name.")

    def validate_last_name(self, last_name):
        if re.fullmatch(r"^(\s)*[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*(\s)*$", last_name.data) is None:
            raise ValidationError("Please insert a last name.")


class LoginForm(FlaskForm):
    email = StringField("Email", [validators.Length(
        min=4, max=40), validators.Email(message="Email address format is incorrect."), validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])

    def validate_password(self, password):
        try:
            SQL = """SELECT password FROM users WHERE email=:email;"""
            hash = db.session.execute(
                SQL, {"email": self.email.data.lower()}).fetchone()[0]
            if not check_password_hash(hash, password.data):
                raise ValidationError("Your email or password is incorrect.")
        except: raise ValidationError("Your email or password is incorrect.")
