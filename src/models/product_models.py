from flask_sqlalchemy import SQLAlchemy
from src.__init__ import app
marketplace_db = SQLAlchemy(app)


class FilterManager:
    def __init__(
        self,
        condition="Any (default)",
        category="Any (default)",
        sort="A-Z (default)",
        search=""
    ):
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
        if self.condition == "Any (default)" and self.category == "Any (default)":
            sql = """
            SELECT
            id, title, details, condition, price, username
            FROM products
            WHERE (isSold=FALSE AND
            title iLIKE (CASE WHEN :search != '' THEN :search END))
            ORDER BY
            (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
            (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
            (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
            (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
            (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = marketplace_db.session.execute(
                sql,
                {"condition": self.condition,
                 "category": self.category,
                 "sort": self.sort,
                 "search": "%"+self.search+"%"
                 }
            ).fetchall()

        elif self.condition != "Any (default)" and self.category == "Any (default)":
            sql = """
            SELECT id, title, details, condition, price, username
            FROM products
            WHERE
            (isSold=FALSE AND condition=:condition
            AND
            title iLIKE (CASE WHEN :search != '' THEN :search END))
            ORDER BY
            (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
            (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
            (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
            (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
            (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = marketplace_db.session.execute(
                sql,
                {"condition": self.condition,
                 "category": self.category,
                 "sort": self.sort,
                 "search": "%"+self.search+"%"}).fetchall()

        elif self.condition == "Any (default)" and self.category != "Any (default)":
            sql = """
            SELECT id, title, details, condition, price, username
            FROM products
            WHERE (isSold=FALSE AND category=:category AND title iLIKE (CASE WHEN :search != '' THEN :search END))
            ORDER BY
            (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
            (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
            (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
            (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
            (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = marketplace_db.session.execute(
                sql, {"condition": self.condition,
                      "category": self.category,
                      "sort": self.sort,
                      "search": "%"+self.search+"%"}).fetchall()

        elif self.condition != "Any (default)" and self.category != "Any (default)":
            sql = """
            SELECT id, title, details, condition, price, username
            FROM products
            WHERE isSold=FALSE AND condition=:condition AND category=:category AND title iLIKE (CASE WHEN :search != '' THEN :search END)
            ORDER BY
            (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
            (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
            (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
            (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
            (CASE WHEN :sort = 'A-Z (default)' THEN title END) ASC;"""
            data = marketplace_db.session.execute(
                sql, {"condition": self.condition,
                      "category": self.category,
                      "sort": self.sort,
                      "search": "%"+self.search+"%"}).fetchall()
        marketplace_db.session.commit()
        self.search = ""
        return data


class ProductManager:
    def __init__(self, username=None, product_id=None):
        self.product_id = product_id
        self.username = username
        self.title = None
        self.details = None
        self.price = None
        self.category = None
        self.condition = None

    def set_product_info(self, product_info=None):
        if product_info is not None:
            self.title = product_info["title"]
            self.details = product_info["details"]
            self.price = product_info["price"]
            self.category = product_info["category"]
            self.condition = product_info["condition"]

    def insert_product_imgs(self, img_id):
        sql = "INSERT INTO product_images(image_id, product_id) VALUES (:image_id, :product_id);"
        marketplace_db.session.execute(
            sql, {"product_id": self.product_id, "image_id": img_id})
        marketplace_db.session.commit()

    def insert_product(self):
        sql = """INSERT INTO products(id, title, details, condition, category, price, username)
        VALUES(:id, :title, :details, :condition, :category, :price, :username);"""
        marketplace_db.session.execute(sql,
                                       {"id": self.product_id,
                                        "title": self.title,
                                        "details": self.details,
                                        "condition": self.condition,
                                        "category": self.category,
                                        "price": self.price,
                                        "username": self.username})
        marketplace_db.session.commit()

    def update_title(self):
        sql = """UPDATE products SET title=:title WHERE id=:product_id;"""
        marketplace_db.session.execute(
            sql, {"title": self.title, "product_id": self.product_id, })
        marketplace_db.session.commit()

    def update_details(self):
        sql = """UPDATE products SET details=:details WHERE id=:product_id;"""
        marketplace_db.session.execute(
            sql, {"product_id": self.product_id, "details": self.details})
        marketplace_db.session.commit()

    def update_price(self):
        sql = """UPDATE products SET price=:price WHERE id=:product_id;"""
        marketplace_db.session.execute(
            sql, {"product_id": self.product_id, "price": self.price})
        marketplace_db.session.commit()

    def update_category(self):
        sql = """UPDATE products SET category=:category WHERE id=:product_id;"""
        marketplace_db.session.execute(
            sql, {"product_id": self.product_id, "category": self.category})
        marketplace_db.session.commit()

    def update_condition(self):
        sql = """UPDATE products SET condition=:condition WHERE id=:product_id;"""
        marketplace_db.session.execute(
            sql, {"product_id": self.product_id, "condition": self.condition})
        marketplace_db.session.commit()


def fetch_issold(product_id):
    sql = """SELECT isSold
    FROM products
    WHERE id=:product_id;"""
    return marketplace_db.session.execute(sql,
                                          {"product_id": product_id}).fetchone()[0]


def update_issold(sold_to, is_sold: bool, product_id):
    sql = """UPDATE products
    SET isSold=:isSold, sold_to=:sold_to
    WHERE id=:product_id;"""
    marketplace_db.session.execute(sql,
                                   {"product_id": product_id,
                                    "isSold": is_sold,
                                    "sold_to": sold_to})
    marketplace_db.session.commit()


def fetch_product_imgs(product_id):
    sql = "SELECT image_id FROM product_images WHERE product_id=:product_id;"
    return marketplace_db.session.execute(
        sql, {"product_id": product_id}).fetchall()


def fetch_product_img(product_id):
    sql = """
    SELECT image_id
    FROM product_images
    WHERE product_id=:product_id 
    ORDER BY RANDOM() LIMIT 1;
    """
    data = marketplace_db.session.execute(sql,
                                          {"product_id": product_id}).fetchone()
    if data is not None and data.image_id is not None:
        return data.image_id
    return "default.png"


def check_product_exists(product_id):
    sql = """SELECT exists (SELECT id FROM products WHERE id=:product_id);"""
    return marketplace_db.session.execute(sql,
                                          {"product_id": product_id}).fetchone()[0]


def fetch_product(product_id):
    sql = """
    SELECT id, title, details, condition, category, price, username
    FROM products
    WHERE id =:product_id"""
    return marketplace_db.session.execute(sql,
                                          {"product_id": product_id}).fetchone()


def fetch_bought_products(sold_to):
    sql = """SELECT id, title, price, username FROM products WHERE sold_to=:sold_to"""
    return marketplace_db.session.execute(sql, {"sold_to": sold_to}).fetchall()


def fetch_user_products(username):
    sql = """SELECT id, title, price, username
    FROM products
    WHERE isSold=False AND username=:username"""
    return marketplace_db.session.execute(sql,
                                          {"username": username}).fetchall()


def fetch_sold_products(username):
    sql = """SELECT id, title, price, username, sold_to
    FROM products
    WHERE isSold=True AND username=:username"""
    return marketplace_db.session.execute(sql,
                                          {"username": username}).fetchall()


def count_sold_products(username):
    sql = """SELECT count(*) FROM products
    WHERE username=:username and isSold=True;"""
    return marketplace_db.session.execute(sql,
                                          {"username": username}).fetchone()[0]


def delete_product(product_id):
    sql = """DELETE FROM products
    WHERE id=:product_id;"""
    marketplace_db.session.execute(sql,
                                   {"product_id": product_id})
    marketplace_db.session.commit()


def delete_product_images(product_id):
    sql = """DELETE FROM product_images WHERE product_id=:product_id;"""
    marketplace_db.session.execute(sql, {"product_id": product_id})
    marketplace_db.session.commit()
