import json
from flask_login import UserMixin
from uuid import uuid4
from flask import flash
from routes import db

class User(UserMixin):
    def __init__(self, user_id, username, password, first_name, profile_picture_id="default.jpg", active=True, authenticated=True):
        self.user_id = user_id
        self.username = username
        self.profile_picture_id = profile_picture_id
        self.password = password
        self.first_name = first_name
        self.authenticated = authenticated
        self.active = active
    
    def create_user(self, email, last_name, street_address, phone_number, country, city, province, postal_code, birthday):
        try:
            SQL = """INSERT INTO users (username, email, password, first_name, last_name, street_address, phone_number, country, city, province, postal_code, birthday)
                VALUES (:username, :email, :password, :first_name, :last_name, :street_address, :phone_number,
                :country, :city, :province, :postal_code, :birthday)"""

            db.session.execute(SQL, {"username": self.username,"email": email, "password": self.password,
                                "first_name": self.first_name, "last_name": last_name, "street_address": street_address,
                                "phone_number": phone_number, "country":country, "city": city, "province": province, "postal_code": postal_code, "birthday": birthday})
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong with user creation: {error}")
    
    def get_user_information(self):
        try:
            SQL  = """SELECT first_name, last_name, email, street_address, phone_number, country, city, province, postal_code FROM users WHERE username=:username;"""
            data = db.session.execute(SQL, {"username":self.username}).fetchone()
            if data:
                response_object = { 
                "first_name": data[0],
                "last_name": data[1],
                "email": data[2], 
                "street_address": data[3],
                "phone_number": data[4],
                "country": data[5], 
                "city": data[6],
                "province": data[7],
                "postal_code": data[8]
                }
                return response_object
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong with fetching user data: {error}.")
    
    def fetch_user(username):
        try:
            SQL = """SELECT password, first_name FROM users WHERE username=:username;"""
            data = db.session.execute(SQL, {"username":username.lower()}).fetchone()
            if data:
                password = data[0]
                first_name = data[1]
                return User(user_id=uuid4(),username=username,password=password,first_name=first_name)
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong fetching user: {error}.")
    
    def get_password(username):
        try:
            SQL = """SELECT password FROM users WHERE username=:username;"""
            hash = db.session.execute(SQL, {"username": username.lower()}).fetchone()[0]
            db.session.commit()
            return hash
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong fetching password: {error}.")
    
    def check_email(email):
        try:
            SQL = "SELECT EXISTS(SELECT email FROM users WHERE email=:email);"
            db_email = db.session.execute(SQL, {"email": email.lower()}).fetchone()[0]
            db.session.commit()
            if db_email:
                return True
            return False
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong checking email: {error}")
    
    def check_username(username):
        try:
            SQL = "SELECT EXISTS(SELECT username FROM users WHERE username=:username);"
            db_username = db.session.execute(SQL, {"username": username.lower()}).fetchone()[0]
            db.session.commit()
            if db_username:
                return True
            return False
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong checking username: {error}")

    def create_session(user):
        try:
            SQL = """INSERT INTO sessions (user_id, username, password, first_name, active, authenticated)
            VALUES (:user_id, :username, :password, :first_name, :active, :authenticated );"""
            db.session.execute(SQL, {"user_id":user.user_id, "username":user.username, "password":user.password, "first_name":user.first_name, "active":user.active, "authenticated":user.authenticated})
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong session creation: {error}")
    
    def delete_session(user):
        try:
            SQL = """DELETE FROM sessions WHERE user_id=user_id;"""
            db.session.execute(SQL, {"user_id":user.user_id})
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            flash(f"Something went wrong deleting session: {error}")

    def get(user_id):
        try:
            SQL = """SELECT user_id, username, password, first_name, active, authenticated FROM sessions WHERE
            user_id=:user_id"""
            data = db.session.execute(SQL, {"user_id":user_id}).fetchone()
            db.session.commit()

            if data:
                user_id = data[0]
                username = data[1]
                password = data[2]
                first_name = data[3]
                active = data[4]
                authenticated = data[5]
                return User(user_id, username, password, first_name, active=active, authenticated=authenticated)
        except Exception as error:
            flash(f"Something went wrong with fetching user object: {error}")
            return None

    def get_id(self):
        return str(self.user_id)
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return self.active

