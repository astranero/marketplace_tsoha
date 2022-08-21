from flask_login import UserMixin
from uuid import uuid4
from flask import flash
from routes import db
from marketplace_managers import FilterManager


class User(UserMixin):
    def __init__(self, user_id, username, password, first_name, profile_picture_id="default.png", issuperuser=False, active=True, authenticated=True):
        self.user_id = user_id
        self.username = username.lower()
        self.profile_picture_id = profile_picture_id
        self.password = password
        self.first_name = first_name
        self.authenticated = authenticated
        self.issuperuser = issuperuser
        self.active = active

    def create_user(self, email, last_name, street_address, phone_number, country, city, province, postal_code, birthday):
        SQL = """INSERT INTO users (username, email, password, first_name,  last_name, street_address, phone_number, country, city, province, postal_code, birthday,  profile_picture_id)
            VALUES (:username, :email, :password, :first_name, :last_name,  :street_address, :phone_number,
            :country, :city, :province, :postal_code, :birthday, :profile_picture_id)"""

        db.session.execute(SQL, {"username": self.username.lower(), "email": email.lower(), "password": self.password,
                                 "first_name": self.first_name, "last_name": last_name, "profile_picture_id": self.profile_picture_id, "street_address": street_address,
                                 "phone_number": phone_number, "country": country, "city": city, "province": province, "postal_code": postal_code, "birthday": birthday})
        db.session.commit()
        return True

    def get_user_information(self):
        SQL = """SELECT first_name, last_name, email, street_address, phone_number, country, city, province, postal_code FROM users WHERE username=:username;"""
        data = db.session.execute(
            SQL, {"username": self.username}).fetchone()
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
        else:
            return None

    def update_first_name(username, first_name):
        SQL = "UPDATE users SET first_name=:first_name WHERE username=:username;"
        db.session.execute(
            SQL, {"first_name": first_name, "username": username})
        db.session.commit()

    def update_last_name(username, last_name):
        SQL = "UPDATE users SET last_name=:last_name WHERE username=:username;"
        db.session.execute(SQL, {"last_name": last_name, "username": username})
        db.session.commit()

    def update_email(username, email):
        SQL = "UPDATE users SET email=:email WHERE username=:username;"
        db.session.execute(SQL, {"email": email, "username": username})
        db.session.commit()

    def update_street_address(username, street_address):
        SQL = "UPDATE users SET street_address=:street_address WHERE username=:username;"
        db.session.execute(
            SQL, {"street_address": street_address, "username": username})
        db.session.commit()

    def update_phone_number(username, phone_number):
        SQL = "UPDATE users SET phone_number=:phone_number WHERE username=:username;"
        db.session.execute(
            SQL, {"phone_number": phone_number, "username": username})
        db.session.commit()

    def update_country(username, country):
        SQL = "UPDATE users SET country=:country WHERE username=:username;"
        db.session.execute(SQL, {"country": country, "username": username})
        db.session.commit()

    def update_city(username, city):
        SQL = "UPDATE users SET city=:city WHERE username=:username;"
        db.session.execute(SQL, {"city": city, "username": username})
        db.session.commit()

    def update_province(username, province):
        SQL = "UPDATE users SET province=:province WHERE username=:username;"
        db.session.execute(SQL, {"province": province, "username": username})
        db.session.commit()

    def update_postal_code(username, postal_code):
        SQL = "UPDATE users SET postal_code=:postal_code WHERE username=:username;"
        db.session.execute(
            SQL, {"postal_code": postal_code, "username": username})
        db.session.commit()

    def update_password(username, password):
        SQL = "UPDATE users SET password=:password WHERE username=:username;"
        db.session.execute(SQL, {"password": password, "username": username})
        db.session.commit()

    def update_profile_picture(self, username, profile_picture_id):
        self.profile_picture_id = profile_picture_id
        SQL = "UPDATE users SET profile_picture_id=:profile_picture_id WHERE username=:username;"
        db.session.execute(
            SQL, {"profile_picture_id": profile_picture_id, "username": username.lower()})
        SQL = "UPDATE sessions SET profile_picture_id=:profile_picture_id WHERE username=:username;"
        db.session.execute(
            SQL, {"profile_picture_id": profile_picture_id, "username": username.lower()})
        self.profile_picture_id = profile_picture_id
        db.session.commit()

    def fetch_user(username):
        SQL = """SELECT password, profile_picture_id, first_name FROM users WHERE username=:username;"""
        data = db.session.execute(
            SQL, {"username": username.lower()}).fetchone()
        if data:
            password = data[0]
            profile_picture_id = data[1]
            first_name = data[2]
            return User(user_id=uuid4(), username=username, profile_picture_id=profile_picture_id, password=password, first_name=first_name)

    def fetch_profile_picture(self, username):
        SQL = "SELECT profile_picture_id FROM users WHERE username=:username;"
        profile_picture_id = db.session.execute(
            SQL, {"username": username.lower()}).fetchone()[0]
        db.session.commit()
        return profile_picture_id

    def get_password(username):
        SQL = """SELECT password FROM users WHERE username=:username;"""
        hash = db.session.execute(
            SQL, {"username": username.lower()}).fetchone()[0]
        db.session.commit()
        return hash

    def check_email(email):
        SQL = "SELECT EXISTS(SELECT email FROM users WHERE email=:email);"
        db_email = db.session.execute(
            SQL, {"email": email.lower()}).fetchone()[0]
        db.session.commit()
        if db_email:
            return True
        return False

    def fetch_email(username):
        SQL = "SELECT email FROM users WHERE username=:username;"
        db_email = db.session.execute(
            SQL, {"username": username}).fetchone()[0]
        db.session.commit()
        return db_email

    def check_username(username):
        SQL = "SELECT EXISTS(SELECT username FROM users WHERE username=:username);"
        db_username = db.session.execute(
            SQL, {"username": username.lower()}).fetchone()[0]
        db.session.commit()
        if db_username:
            return True
        return False

    def create_session(user):
        SQL = """INSERT INTO sessions (user_id, username, password, profile_picture_id, first_name, active, authenticated)
            VALUES (:user_id, :username, :password, :profile_picture_id, :first_name, :active, :authenticated );"""
        db.session.execute(SQL, {"user_id": user.user_id, "username": user.username, "password": user.password,
                           "first_name": user.first_name, "active": user.active, "profile_picture_id": user.profile_picture_id, "authenticated": user.authenticated})
        db.session.commit()

    def delete_session(user):
        SQL = """DELETE FROM sessions WHERE user_id=user_id;"""
        db.session.execute(SQL, {"user_id": user.user_id})
        db.session.commit()

    def delete_profile(self):
        sql = """DELETE FROM users WHERE username=:username;"""
        db.session.execute(sql, {"username": self.username})

    def get(user_id):
        try:
            SQL = """SELECT user_id, username, password, first_name, profile_picture_id, active, authenticated FROM sessions WHERE
            user_id=:user_id"""
            data = db.session.execute(SQL, {"user_id": user_id}).fetchone()
            db.session.commit()

            if data:
                user_id = data[0]
                username = data[1]
                password = data[2]
                first_name = data[3]
                profile_picture_id = data[4]
                active = data[5]
                authenticated = data[6]
                return User(user_id, username, password, first_name, profile_picture_id=profile_picture_id, active=active, authenticated=authenticated)
        except Exception as error:
            flash(f"Something went wrong with fetching user object: {error}")
            return None

    def get_profile_picture(username):
        SQL = "SELECT profile_picture_id FROM users WHERE username=:username;"
        profile_picture_id = db.session.execute(
            SQL,  {"username": username}).fetchone()[0]
        db.session.commit()
        return profile_picture_id

    def like_profile(self, liker_username, profile_username, islike):
        sql = "INSERT INTO likes (liker_username, profile_username, islike) VALUES (:liker_username, :profile_username, :islike);"
        db.session.execute(sql, {"liker_username": liker_username,
                           "profile_username": profile_username, "islike": islike})
        db.session.commit()

    def fetch_profile_islike(self, liker_username, profile_username):
        sql = "SELECT islike FROM likes WHERE profile_username=:profile_username AND liker_username=:liker_username;"
        islike = db.session.execute(
            sql, {"liker_username": liker_username, "profile_username": profile_username}).fetchone()
        if islike:
            return islike[0]

    def has_liked_profile(self, liker_username, profile_username):
        sql = "SELECT EXISTS (SELECT 1 FROM likes WHERE profile_username=:profile_username AND liker_username=:liker_username);"
        has_liked = db.session.execute(
            sql, {"liker_username": liker_username, "profile_username": profile_username}).fetchone()
        if has_liked:
            return has_liked[0]
        return False

    def update_profile_like(self, liker_username, profile_username, islike):
        sql = "UPDATE likes SET islike=:islike WHERE liker_username=:liker_username AND profile_username=:profile_username; "
        db.session.execute(sql, {"liker_username": liker_username,
                           "profile_username": profile_username, "islike": islike})
        db.session.commit()

    def count_profile_likes(self, profile_username):
        sql = "SELECT count(islike) FROM likes WHERE islike=True AND profile_username=:profile_username;"
        return db.session.execute(sql, {"profile_username": profile_username}).fetchone()[0]

    def get_id(self):
        return str(self.user_id)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active
