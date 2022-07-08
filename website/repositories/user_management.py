 
from werkzeug.security import generate_password_hash
from website.__init__ import db

def create_user(email, first_name, last_name, password, street_address, phone_number, city, state_prov, postal_code, birth_date):
       hash_value = generate_password_hash(password)
       sql ="""INSERT INTO users (email, password, first_name, last_name,street_address,phone_number, city, state_prov, postal_code, birth_date)
        VALUES (:email, :hash_value, :first_name, :last_name, :street_address, :phone_number,
        :city, :state_prov, :postal_code, :birth_date)"""

       db.session.execute(sql, {"email":email, "hash_value":hash_value, 
       "first_name":first_name, "last_name":last_name, "street_address":street_address,
       "phone_number":phone_number, "city":city, "state_prov":state_prov, "postal_code":postal_code, "birth_date":birth_date})
       db.session.commit()

def find_password(email):
       sql = """SELECT hash_value FROM users WHERE email=:email;"""
       hash_value = db.session.execute(sql, {"email":email}).fetchone()
       return hash_value
