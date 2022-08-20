from routes import db
from flask import flash


class FilterManager:
    def __init__(self, condition="Any (default)", category="Any (default)", sort="A-Z (default)", search=""):
        self.condition = condition
        self.category = category
        self.sort = sort
        self.search = search

    def set_condition(self, condition):
        self.condition = condition

    def set_category(self, category):
        self.category = category

    def set_sort(self, sort):
        self.sort = sort

    def set_search(self, search):
        self.search = search

    def fetch_products(self):
        flash(self.search)
        if self.condition == "Any (default)" and self.category == "Any (default)":
            SQL = """SELECT id, title, details, condition, price, username
        FROM products WHERE (isSold=FALSE AND title iLIKE (CASE WHEN :search != '' THEN :search END))
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort, "search": "%"+self.search+"%"}).fetchall()

        elif self.condition != "Any (default)" and self.category == "Any (default)":
            SQL = """
        SELECT id, title, details, condition, price, username
        FROM products
        WHERE (isSold=FALSE AND condition=:condition AND title iLIKE (CASE WHEN :search != '' THEN :search END))
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort, "search": "%"+self.search+"%"}).fetchall()

        elif self.condition == "Any (default)" and self.category != "Any (default)":
            SQL = """
        SELECT id, title, details, condition, price, username
        FROM products
        WHERE (isSold=FALSE AND category=:category AND title iLIKE (CASE WHEN :search != '' THEN :search END))
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort, "search": "%"+self.search+"%"}).fetchall()

        elif self.condition != "Any (default)" and self.category != "Any (default)":
            SQL = """
        SELECT id, title, details, condition, price, username
        FROM products
        WHERE isSold=FALSE AND condition=:condition AND category=:category AND title iLIKE (CASE WHEN :search != '' THEN :search END)
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort, "search": "%"+self.search+"%"}).fetchall()
        db.session.commit()
        self.search = ""
        return data


class ProductManager:
    def __init__(self, product_id, username, title, details, price, category, condition):
        self.product_id = product_id
        self.username = username
        self.title = title
        self.details = details
        self.price = price
        self.category = category
        self.condition = condition

    def insert_product_imgs(self, img_id):
        SQL = "INSERT INTO product_images(image_id, product_id) VALUES (:image_id, :product_id);"
        db.session.execute(
            SQL, {"product_id": self.product_id, "image_id": img_id})
        db.session.commit()

    def fetch_product_imgs(product_id):
        SQL = "SELECT image_id FROM product_images WHERE product_id=:product_id;"
        data = db.session.execute(SQL, {"product_id": product_id}).fetchall()
        db.session.commit()
        return data

    def fetch_product_img(product_id):
        SQL = "SELECT image_id FROM product_images WHERE product_id=:product_id ORDER BY RANDOM() LIMIT 1;"
        data = db.session.execute(SQL, {"product_id": product_id}).fetchone()
        return data[0]

    def fetch_product(product_id):
        SQL = """SELECT id, title, details, condition, category, price, username FROM products WHERE id =:product_id"""
        return db.session.execute(SQL, {"product_id": product_id}).fetchone()

    def insert_product(self):
        SQL = """INSERT INTO products(id, title, details, condition, category, price, username)
        VALUES(:id, :title, :details, :condition, :category, :price, :username);"""
        db.session.execute(SQL, {"id": self.product_id, "title": self.title, "details": self.details, "condition": self.condition,
                           "category": self.category, "price": self.price, "username": self.username})
        db.session.commit()

    def delete_product(product_id):
        SQL = """DELETE FROM products WHERE id=:product_id;"""
        db.session.execute(SQL, {"product_id": product_id})
        db.session.commit()

    def update_title(product_id, title):
        SQL = """UPDATE products SET title=:title WHERE id=:product_id;"""
        db.session.execute(SQL, {"product_id": product_id, })
        db.session.commit()

    def update_details(product_id, details):
        SQL = """UPDATE products SET details=:details WHERE id=:product_id;"""
        db.session.execute(SQL, {"product_id": product_id, "details": details})
        db.session.commit()

    def update_price(product_id, price):
        SQL = """UPDATE products SET price=:price WHERE id=:product_id;"""
        db.session.execute(SQL, {"product_id": product_id, "price": price})
        db.session.commit()

    def update_category(product_id, category):
        SQL = """UPDATE products SET category=:category WHERE id=:product_id;"""
        db.session.execute(
            SQL, {"product_id": product_id, "category": category})
        db.session.commit()

    def update_condition(product_id, condition):
        SQL = """UPDATE products SET condition=:condition WHERE id=:product_id;"""
        db.session.execute(
            SQL, {"product_id": product_id, "condition": condition})
        db.session.commit()

    def update_isSold(product_id, isSold, sold_to):
        SQL = """UPDATE products SET isSold=:isSold, sold_to=:sold_to 
        WHERE id=:product_id;"""
        db.session.execute(SQL, {"product_id":product_id, "isSold":isSold, "sold_to":sold_to})
        db.session.commit()
