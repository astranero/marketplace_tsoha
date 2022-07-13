import json
from flask_login import UserMixin
from uuid import uuid4
from flask import flash
from routes import db

class User(UserMixin):
    def __init__(self, user_id, username, password, first_name, last_name, active=True, authenticated=True):
        self.user_id = user_id
        self.user_name = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.authenticated = authenticated
        self.active = active
    
    def create_user(self, street_address, phone_number, city, state_prov, postal_code, birth_date):
        try:
            SQL = """INSERT INTO users (username, email, password, first_name, last_name,street_address,phone_number, city, state_prov, postal_code, birth_date)
                VALUES (:email, :password, :first_name, :last_name, :street_address, :phone_number,
                :city, :state_prov, :postal_code, :birth_date)"""

            db.session.execute(SQL, {"username": self.username,"email": self.email, "password": self.password,
                                "first_name": self.first_name, "last_name": self.last_name, "street_address": street_address,
                                "phone_number": phone_number, "city": city, "state_prov": state_prov, "postal_code": postal_code, "birth_date": birth_date})
            db.session.commit()
        except:
            db.session.rollback()
            flash("Something went wrong with user creation, please report it.")
    
    def get_user_information(self):
        try:
            SQL  = """SELECT email, street_address, phone, country, city, province, postal_code FROM users WHERE username=:username;"""
            data = db.session.execute(SQL, {"email":self.username}).fetchone()
            if data:
                response_object = { "email": data[0], 
                "street_address": data[1],
                "phone": data[2],
                "country": data[3], 
                "province": data[4]
                }
                return json.dumps(response_object)
        except Exception as error:
            db.session.rollback()
            flash(f"{error}")
    
    def fetch_user(username):
        try:
            SQL = """SELECT password, first_name, last_name FROM users WHERE username=:username;"""
            data = db.session.execute(SQL, {"username":username}).fetchone()
            if data:
                password = data[0]
                first_name = data[1]
                last_name = data[2]
                return User(user_id=uuid4(),username=username,password=password,first_name=first_name,last_name=last_name)
        except:
            db.session.rollback()
            flash("Something went wrong, please try again.")
    
    def get_password(username):
        try:
            SQL = """SELECT password FROM users WHERE username=:username;"""
            hash = db.session.execute(SQL, {"email": username}).fetchone()[0]
            db.session.commit()
            return hash
        except:
            db.session.rollback()
            flash("Something went wrong, please try again.")
    
    def check_email(email):
        try:
            SQL = "SELECT EXISTS(SELECT email FROM users WHERE email=:email);"
            db_email = db.session.execute(SQL, {"email": email.lower()}).fetchone()[0]
            db.session.commit()
            if db_email:
                return True
            return False
        except:
            db.session.rollback()
            flash("Something went wrong: Are you sure user exists?")
    
    def check_username(username):
        try:
            SQL = "SELECT EXISTS(SELECT username FROM users WHERE username=:username);"
            username = db.session.execute(SQL, {"email": username}).fetchone()[0]
            db.session.commit()
            if username:
                return True
            return False
        except:
            db.session.rollback()
            flash("Something went wrong: Are you sure user exists?")

    def create_session(user):
        try:
            SQL = """INSERT INTO sessions (user_id, password, first_name, last_name, active, authenticated, is_banned)
            VALUES (:user_id, :email, :password, :first_name, :last_name, :active, :authenticated, :is_banned);"""
            db.session.execute(SQL, {"user_id":user.user_id, "email":user.email, "password":user.password, "first_name":user.first_name,
            "last_name":user.last_name, "active":user.active, "authenticated":user.authenticated, "is_banned":user.is_banned})
            db.session.commit()
        except:
            db.session.rollback()
            flash("Something went wrong with session creation.")
    
    def delete_session(user):
        try:
            SQL = """DELETE FROM sessions WHERE user_id=user_id;"""
            db.session.execute(SQL, {"user_id":user.user_id})
            db.session.commit()
        except:
            db.session.rollback()
            flash("Something went wrong with session deletion.")
    
    def get(user_id):
        try:
            SQL = """SELECT user_id, username, password, first_name, last_name, active, authenticated, is_banned FROM sessions WHERE
            user_id=:user_id"""
            data = db.session.execute(SQL, {"user_id":user_id}).fetchone()
            db.session.commit()

            if data:
                user_id = data[0]
                username = data[1]
                password = data[2]
                first_name = data[3]
                last_name = data[4]
                active = data[5]
                authenticated = data[6]
                is_banned = data[7]
                return User(user_id, username, password, first_name, last_name, active=active, authenticated=authenticated, is_banned=is_banned)
        except:
            return None

    def get_id(self):
        return str(self.user_id)
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return self.active
    