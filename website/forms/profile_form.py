from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    validators,
    TelField, ValidationError,
    EmailField
)
from flask_login import current_user
from models.user_model import check_email

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
