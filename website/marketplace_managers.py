from routes import db


class FilterManager:
    def __init__(self, condition="Any", category="Any", sort="A-Z (default)"):
        self.condition = condition
        self.category = category
        self.sort = sort

    def set_condition(self, condition):
        self.condition = condition

    def set_category(self, category):
        self.category = category

    def set_sort(self, sort):
        self.sort = sort

    def fetch_products(self):
        if self.condition == "Any" and self.category == "Any":
            SQL = """SELECT id, title, details, condition, price, best_offer, offerer, username
        FROM products WHERE isSold=FALSE    
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) DESC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort}).fetchall()

        elif self.condition != "Any" and self.category == "Any":
            SQL = """
        SELECT id, title, details, condition, price, best_offer, offerer, username
        FROM products
        WHERE isSold=FALSE AND condition=:condition
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) DESC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort}).fetchall()

        elif self.condition == "Any" and self.category != "Any":
            SQL = """
        SELECT id, title, details, condition, price, best_offer, offerer, username
        FROM products
        WHERE isSold=FALSE AND category=:category
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) DESC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort}).fetchall()

        elif self.condition != "Any" and self.category != "Any":
            SQL = """
        SELECT id, title, details, condition, price, best_offer, offerer, username
        FROM products
        WHERE isSold=FALSE AND condition=:condition AND category=:category
        ORDER BY
        (CASE WHEN :sort = 'Date - Newest' THEN creation_date END) DESC,
        (CASE WHEN :sort = 'Date - Oldest' THEN creation_date END) ASC,
        (CASE WHEN :sort = 'Price - Highest' THEN price END) DESC,
        (CASE WHEN :sort = 'Price - Lowest' THEN price END) ASC,
        (CASE WHEN :sort = 'A-Z (default)' THEN title END) DESC;"""
            data = db.session.execute(
                SQL, {"condition": self.condition, "category": self.category, "sort": self.sort}).fetchall()
        db.session.commit()
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
        db.session.execute(SQL, {"product_id": product_id})
        db.session.commit()

    def insert_product(self):
        SQL = """INSERT INTO products(id, title, details, condition, category, price, username)
        VALUES(:id, :title, :details, :condition, :category, :price, :username);"""
        db.session.execute(SQL, {"id": self.product_id, "title": self.title, "details": self.details, "condition": self.condition,
                           "category": self.category, "price": self.price, "username": self.username})
        db.session.commit()
