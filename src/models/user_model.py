from uuid import uuid4
from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from src.__init__ import app
user_db = SQLAlchemy(app)


class User(UserMixin):
    def __init__(self, user_id, user_info,
                 profile_picture_id="default.png",
                 authenticated=True,
                 active=True,
                 admin=False):
        self.user_id = user_id
        self.profile_picture_id = profile_picture_id
        self.password = user_info["password"]
        self.first_name = user_info["first_name"]
        self.username = user_info["username"].lower()
        self.authenticated = authenticated
        self.active = active
        self.admin = admin

    def get(self, user_id):
        sql = """SELECT user_id, username, password,
            first_name, profile_picture_id, active, authenticated, admin
            FROM sessions WHERE
            user_id=:user_id"""
        data = user_db.session.execute(sql, {"user_id": user_id}).fetchone()
        user_db.session.commit()
        if data:
            user_id = data[0]
            username = data[1]
            password = data[2]
            first_name = data[3]
            profile_picture_id = data[4]
            active = data[5]
            authenticated = data[6]
            admin = data[7]
            user_info = {
                "password": password,
                "first_name": first_name,
                "username": username
            }
            return User(user_id,
                        user_info,
                        profile_picture_id=profile_picture_id,
                        active=active,
                        authenticated=authenticated,
                        admin=admin)
        return None

    def get_id(self):
        return str(self.user_id)

    def set_profile_picture(self, profile_picture_id):
        self.profile_picture_id = profile_picture_id

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    def create_session(self, user):
        sql = """INSERT INTO sessions
        (user_id, username, password,
        profile_picture_id, first_name, active, authenticated, admin)
        VALUES
        (:user_id, :username, :password,
        :profile_picture_id, :first_name,
        :active, :authenticated, :admin );"""
        user_db.session.execute(sql,
                                {"user_id": user.user_id,
                                 "username": user.username,
                                 "password": user.password,
                                 "first_name": user.first_name,
                                 "active": user.active,
                                 "profile_picture_id": user.profile_picture_id,
                                 "authenticated": user.authenticated,
                                 "admin": user.is_admin})
        user_db.session.commit()

    def delete_session(self):
        sql = """DELETE FROM sessions
        WHERE user_id=user_id;"""
        user_db.session.execute(sql, {"user_id": self.user_id})
        user_db.session.commit()


class UserManager():
    def __init__(self, username):
        self.username = username

    def create_user(self, registration_info):
        sql = """INSERT INTO users
        (username, email, password, first_name,  last_name, street_address,
        phone_number, country, city, province, postal_code, birthday,  profile_picture_id)
        VALUES
        (:username, :email, :password, :first_name, :last_name,  :street_address, :phone_number,
        :country, :city, :province, :postal_code, :birthday, :profile_picture_id)"""

        user_db.session.execute(sql,
                                {"username": self.username.lower(),
                                 "email": registration_info["email"].lower(),
                                 "password": registration_info["password"],
                                 "first_name": registration_info["first_name"],
                                 "last_name": registration_info["last_name"],
                                 "profile_picture_id": registration_info["profile_picture_id"],
                                 "street_address": registration_info["street_address"],
                                 "phone_number": registration_info["phone_number"],
                                 "country": registration_info["country"],
                                 "city": registration_info["city"],
                                 "province": registration_info["province"],
                                 "postal_code": registration_info["postal_code"],
                                 "birthday": registration_info["birthday"]
                                 }
                                )
        user_db.session.commit()
        return self.fetch_user()

    def fetch_user(self):
        sql = """SELECT password, profile_picture_id, first_name, active, admin
        FROM users
        WHERE username=:username;"""
        data = user_db.session.execute(sql,
                                       {"username": self.username.lower()}).fetchone()
        if data:
            password = data[0]
            profile_picture_id = data[1]
            first_name = data[2]
            active = data[3]
            admin = data[4]
            user_info = {
                "password": password,
                "first_name": first_name,
                "username": self.username}
            return User(user_id=uuid4(),
                        user_info=user_info,
                        profile_picture_id=profile_picture_id,
                        active=active,
                        admin=admin)
        return None

    def get_user_information(self):
        sql = """SELECT first_name, last_name, email, street_address,
        phone_number, country, city, province, postal_code
        FROM users WHERE username=:username;"""
        data = user_db.session.execute(
            sql, {"username": self.username}).fetchone()
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
        return None

    def update_first_name(self, first_name):
        sql = """UPDATE users
        SET first_name=:first_name
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"first_name": first_name,
                                 "username": self.username})
        user_db.session.commit()

    def update_last_name(self, last_name):
        sql = """UPDATE users
        SET last_name=:last_name
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"last_name": last_name,
                                 "username": self.username})
        user_db.session.commit()

    def update_email(self, email):
        sql = """UPDATE users
        SET email=:email
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"email": email,
                                 "username": self.username})
        user_db.session.commit()

    def update_street_address(self, street_address):
        sql = """UPDATE users
        SET street_address=:street_address
        WHERE username=:username;"""
        user_db.session.execute(
            sql, {"street_address": street_address,
                  "username": self.username})
        user_db.session.commit()

    def update_phone_number(self, phone_number):
        sql = """UPDATE users
        SET phone_number=:phone_number
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"phone_number": phone_number,
                                 "username": self.username})
        user_db.session.commit()

    def update_country(self, country):
        sql = """UPDATE users
        SET country=:country
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"country": country,
                                 "username": self.username})
        user_db.session.commit()

    def update_city(self, city):
        sql = """UPDATE users
        SET city=:city
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"city": city,
                                 "username": self.username})
        user_db.session.commit()

    def update_province(self, province):
        sql = """UPDATE users
        SET province=:province
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"province": province,
                                 "username": self.username})
        user_db.session.commit()

    def update_postal_code(self, postal_code):
        sql = """UPDATE users
        SET postal_code=:postal_code
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"postal_code": postal_code,
                                 "username": self.username})
        user_db.session.commit()

    def update_password(self, password):
        sql = """UPDATE users
        SET password=:password
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"password": password,
                                 "username": self.username})
        user_db.session.commit()

    def update_activity(self, active):
        sql = """UPDATE users
        SET active=:active
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"active": active,
                                 "username": self.username})
        user_db.session.commit()

    def update_is_admin(self, admin):
        sql = """UPDATE users
        SET admin=:admin
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"admin": admin,
                                 "username": self.username})
        user_db.session.commit()

    def get_password(self):
        sql = """SELECT password
        FROM users
        WHERE username=:username;"""
        hash_password = user_db.session.execute(
            sql, {"username": self.username.lower()}).fetchone()[0]
        user_db.session.commit()
        return hash_password

    def fetch_email(self):
        sql = """
        SELECT email FROM users
        WHERE username=:username;
        """
        user_db_email = user_db.session.execute(
            sql, {"username": self.username}).fetchone()[0]
        user_db.session.commit()
        return user_db_email


class ProfileManager():
    def __init__(self):
        pass

    def fetch_profile_picture(self, username):
        sql = """SELECT profile_picture_id
            FROM users
            WHERE username=:username;"""
        profile_picture_id = user_db.session.execute(
            sql, {"username": username.lower()}).fetchone()[0]
        user_db.session.commit()
        return profile_picture_id

    def like_profile(self, liker_username, profile_username, islike):
        sql = """INSERT INTO likes (liker_username, profile_username, islike)
        VALUES (:liker_username, :profile_username, :islike);"""
        user_db.session.execute(sql, {"liker_username": liker_username,
                                      "profile_username": profile_username,
                                      "islike": islike})
        user_db.session.commit()

    def fetch_profile_islike(self, liker_username, profile_username):
        sql = """SELECT islike FROM likes
        WHERE profile_username=:profile_username AND liker_username=:liker_username;"""
        islike = user_db.session.execute(sql, {"liker_username": liker_username,
                                               "profile_username": profile_username}).fetchone()
        if islike:
            return islike[0]
        return None

    def has_liked_profile(self, liker_username, profile_username):
        sql = """SELECT EXISTS
        (SELECT 1 FROM likes
        WHERE profile_username=:profile_username AND liker_username=:liker_username);"""
        has_liked = user_db.session.execute(sql,
                                            {"liker_username": liker_username,
                                             "profile_username": profile_username}).fetchone()
        if has_liked:
            return has_liked[0]
        return False

    def update_profile_like(self, liker_username, profile_username, islike):
        sql = """UPDATE likes SET islike=:islike
        WHERE liker_username=:liker_username AND profile_username=:profile_username;"""
        user_db.session.execute(sql, {"liker_username": liker_username,
                                      "profile_username": profile_username,
                                      "islike": islike})
        user_db.session.commit()

    def count_profile_likes(self, profile_username):
        sql = """SELECT count(islike)
        FROM likes
        WHERE islike=True AND profile_username=:profile_username;"""
        return user_db.session.execute(sql, {"profile_username": profile_username}).fetchone()[0]

    def get_profile_picture(self, username):
        sql = "SELECT profile_picture_id FROM users WHERE username=:username;"
        profile_picture_id = user_db.session.execute(
            sql,  {"username": username}).fetchone()[0]
        user_db.session.commit()
        return profile_picture_id

    def update_profile_picture(self, username, profile_picture_id):
        current_user.set_profile_picture(profile_picture_id)
        sql = """UPDATE users
        SET profile_picture_id=:profile_picture_id
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"profile_picture_id": profile_picture_id,
                                 "username": username.lower()})
        sql = """UPDATE sessions
        SET profile_picture_id=:profile_picture_id
        WHERE username=:username;"""
        user_db.session.execute(sql,
                                {"profile_picture_id": profile_picture_id,
                                 "username": username.lower()})
        user_db.session.commit()

    def delete_profile(self, username):
        sql = """DELETE FROM users
            WHERE username=:username;"""
        user_db.session.execute(sql, {"username": username})


def check_username(username):
    sql = """
    SELECT EXISTS
    (SELECT username
    FROM users
    WHERE username=:username);"""
    user_db_username = user_db.session.execute(
        sql, {"username": username.lower()}).fetchone()[0]
    user_db.session.commit()
    if user_db_username:
        return True
    return False


def check_email(email):
    sql = """SELECT EXISTS
    (SELECT email
    FROM users
    WHERE email=:email);"""
    user_db_email = user_db.session.execute(
        sql, {"email": email.lower()}).fetchone()[0]
    user_db.session.commit()
    if user_db_email:
        return True
    return False
