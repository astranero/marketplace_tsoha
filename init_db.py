import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS users''')
cur.execute('CREATE TABLE IF NOT EXISTS users('
            'username TEXT Unique NOT NULL,'
            'email TEXT Unique,'
            'password TEXT NOT NULL,'
            'first_name TEXT,'
            'last_name TEXT,'
            'profile_picture_id TEXT,'
            'street_address TEXT,'
            'phone TEXT NOT NULL,'
            'country TEXT,'
            'city TEXT,'
            'province TEXT,'
            'postal_code TEXT,'
            'hidden BOOLEAN,'
            'birthday DATE NOT NULL);')

cur.execute('''DROP TABLE IF EXISTS sessions''')
cur.execute('CREATE TABLE IF NOT EXISTS sessions('
            'user_id TEXT NOT NULL,'
            'username TEXT,'
            'password TEXT,'
            'first_name TEXT,'
            'profile_picture_id TEXT,'
            'active BOOLEAN,'
            'authenticated BOOLEAN);')

cur.execute('''DROP TABLE IF EXISTS products''')
cur.execute('CREATE TABLE IF NOT EXISTS products('
            'id SERIAL PRIMARY KEY,'
            'title TEXT NOT NULL,'
            'details TEXT NOT NULL,'
            'quality,'
            'price REAL NOT NULL,'
            'best_offer REAL,'
            'publication_date timestamptz);')

cur.execute('DROP TABLE IF EXISTS product_images')
cur.execute('''CREATE TABLE IF NOT EXISTS product_images(
    product_id TEXT, 
    image_id TEXT NOT NULL Unique,
    publication_date timestamptz);''')

cur.execute('''DROP TABLE IF EXISTS comments''')
cur.execute('''CREATE TABLE IF NOT EXISTS comments(
    id SERIAL PRIMARY KEY,
    user_id TEXT, 
    user_comment TEXT,
    publication_date timestamptz NOT NULL
);''')

cur.execute('''DROP TABLE IF EXISTS likes''')
cur.execute('''CREATE TABLE IF NOT EXISTS likes(
    id  SERIAL Primary Key,
    event_username TEXT,
    target_id TEXT,
    like BOOLEAN);
''')

cur.execute('''DROP TABLE IF EXISTS messages''')
cur.execute('''CREATE TABLE IF NOT EXISTS messages(
    id  SERIAL Primary Key,
    receiver TEXT,
    sender TEXT,
    created_at timestamptz,
    message TEXT,
    );
''')

cur.execute('''DROP TABLE IF EXISTS visitor''')
cur.execute('''CREATE table IF NOT EXISTS visitors(
    id SERIAL PRIMARY KEY,
    visitor_id TEXT,
);
''')

conn.commit()
cur.close()
conn.close
