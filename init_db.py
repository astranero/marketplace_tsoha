import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cur = conn.cursor()


cur.execute('''DROP TABLE IF EXISTS comment_likes''')
cur.execute('''DROP TABLE IF EXISTS post_images''')
cur.execute('''DROP TABLE IF EXISTS post_likes''')
cur.execute('''DROP TABLE IF EXISTS posts''')
cur.execute('''DROP TABLE IF EXISTS sessions''')
cur.execute('''DROP TABLE IF EXISTS comments''')
cur.execute('DROP TABLE IF EXISTS product_images')
cur.execute('''DROP TABLE IF EXISTS messages''')
cur.execute('''DROP TABLE IF EXISTS contact_us_messages''')
cur.execute('''DROP TABLE IF EXISTS likes''')
cur.execute('''DROP TABLE IF EXISTS visitors''')
cur.execute('''DROP TABLE IF EXISTS products''')
cur.execute('''DROP TABLE IF EXISTS users''')


def create_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                username TEXT Unique NOT NULL,
                email TEXT Unique,
                password TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                street_address TEXT,
                phone_number TEXT NOT NULL,
                country TEXT,
                city TEXT,
                province TEXT,
                postal_code TEXT,
                hidden BOOLEAN,
                birthday DATE NOT NULL,
                creation_date date DEFAULT NOW(),
                profile_pic_id TEXT DEFAULT 'default.jpg' NOT NULL);
                """)

    cur.execute("""CREATE TABLE IF NOT EXISTS sessions(
                user_id uuid,
                username TEXT NOT NULL,
                password TEXT,
                first_name TEXT,
                profile_picture_id TEXT,
                active BOOLEAN,
                authenticated BOOLEAN);
                """)

    cur.execute("""CREATE TABLE IF NOT EXISTS products(
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                details TEXT NOT NULL,
                condition TEXT,
                price numeric NOT NULL CONSTRAINT positive_price CHECK (price > 0),
                creation_date timestamptz DEFAULT NOW(),
                username TEXT,
                FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE);
                """)

    cur.execute("""CREATE TABLE IF NOT EXISTS product_images(
        image_id TEXT NOT NULL Unique,
        creation_date timestamptz DEFAULT NOW(),
        product_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE);
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS comments(
        id SERIAL PRIMARY KEY,
        user_comment TEXT,
        product_id INTEGER,
        commentor_username TEXT,
        creation_date timestamptz NOT NULL DEFAULT NOW(),
        FOREIGN KEY(commentor_username) REFERENCES users(username) ON DELETE CASCADE,
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
        );
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS likes(
        id  SERIAL Primary Key,
        product_id INTEGER,
        liker_username TEXT,
        FOREIGN KEY(liker_username) REFERENCES users(username) ON DELETE CASCADE,
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
        islike boolean);
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
        id  SERIAL Primary Key,
        receiver TEXT,
        sender TEXT,
        FOREIGN KEY(receiver) REFERENCES users(username) ON DELETE CASCADE,
        FOREIGN KEY(sender) REFERENCES users(username) ON DELETE CASCADE,
        creation_date timestamptz,
        message TEXT);
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS contact_us_messages(
        id  SERIAL Primary Key,
        sender TEXT,
        creation_date timestamptz NOT NULL DEFAULT NOW(),
        message TEXT);
        """)

    cur.execute("""CREATE table IF NOT EXISTS visitors(
        id SERIAL PRIMARY KEY,
        product_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
        visitor_id TEXT);
        """)


create_tables()
conn.commit()
cur.close()
conn.close
