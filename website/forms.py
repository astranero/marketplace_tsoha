from wtforms import Form, BooleanField, StringField, PasswordField, validators, DateTimeField

class RegistrationForm(Form):
    
    birth_date = DateTimeField("Date of Birth", validators=[validators.Length(min=0, max=35), validators.InputRequired("Your Date of Birth is required.")], format="%d-%m-%Y")
    first_name = StringField("First Name", [validators.Length(min=4, max=40)])
    last_name = StringField("Last Name", [validators.Length(min=4, max=40)])
    email = StringField("Email Address", [validators.Length(min=4, max=40), validators.Email(message="This is not a valid email address.")]) 
    password = PasswordField("New Password", [validators.DataRequired(), validators.Length(min=8),
    validators.EqualTo("sec_password", message="Passwords do not match.")])
    sec_password = PasswordField("Repeat Password")
    phone_number = StringField("Your Phone Number")
    street_address = StringField("Street Address")
    state_prov = StringField("State/Province")
    postal_code = StringField("Postal/Zip Code")
    city = StringField("City")

    def validate_email(form, email):
        """Tarkista onko tietokannassa sähköpostia, raise ValidationError("viesti"), jos löytyy"""
        #Muista myös tyhjät merkkijonot
        pass
    
    def validate_age(form, age):
        """Tarkista ikä"""
        pass

class LoginForm(Form):
    email = StringField("Email", [validators.Length(min=4, max=40), validators.Email(message="Email address is incorrect.")])
    password = PasswordField("Password")