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
    'email TEXT Unique NOT NULL,'
    'password TEXT NOT NULL,'
    'first_name TEXT,'
    'last_name TEXT,'
    'street_address TEXT,'
    'phone_number TEXT NOT NULL,'
    'city TEXT,'
    'state_prov TEXT,'
    'postal_code TEXT,'
    'birth_date DATE NOT NULL);')

cur.execute('''DROP TABLE IF EXISTS sessions''')
cur.execute('CREATE TABLE IF NOT EXISTS sessions('
    'user_id TEXT NOT NULL,'
    'email TEXT,'
    'password TEXT,'
    'first_name TEXT,'
    'last_name TEXT,'
    'active BOOLEAN,'
    'authenticated BOOLEAN,'
    'is_banned BOOLEAN);')
    
cur.execute('''DROP TABLE IF EXISTS posts''')
cur.execute('CREATE TABLE IF NOT EXISTS posts('
    'id SERIAL PRIMARY KEY,'
    'title TEXT NOT NULL,'
    'price REAL NOT NULL,'
    'publication_date timestamptz);')

cur.execute('DROP TABLE IF EXISTS post_images')
cur.execute('''CREATE TABLE IF NOT EXISTS post_images(
    id SERIAL PRIMARY KEY,
    image_name TEXT NOT NULL Unique,
    publication_date timestamptz);''')

cur.execute('''DROP TABLE IF EXISTS comments''')
cur.execute('''CREATE TABLE IF NOT EXISTS comments(
    id SERIAL PRIMARY KEY,
    user_comment TEXT,
    publication_date timestamptz NOT NULL
);''')

cur.execute('''DROP TABLE IF EXISTS post_likes''')
cur.execute('''CREATE TABLE IF NOT EXISTS post_likes(
    id  SERIAL Primary Key,
    post_like BOOLEAN);
''')

cur.execute('''DROP TABLE IF EXISTS comment_likes''')
cur.execute('''CREATE TABLE IF NOT EXISTS comment_likes(
    id  SERIAL Primary Key,
    comment_like BOOLEAN);
''')

cur.execute('''DROP TABLE IF EXISTS visitor''')
cur.execute('''CREATE table IF NOT EXISTS visitors(
    id SERIAL PRIMARY KEY
);
''')

conn.commit()
cur.close()
conn.close