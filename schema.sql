
CREATE TABLE IF NOT EXISTS users(
    id SERIAL Primary Key,
    email TEXT Unique NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    street_address TEXT,
    phone_number TEXT NOT NULL,
    city TEXT,
    state_prov TEXT,
    postal_code TEXT,
    birth_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS posts(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    publication_date timestamptz,
    user_id REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS post_images(
    id PRIMARY KEY,
    publication_date timestamptz,
    post_id REFERENCES posts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments(
    id SERIAL PRIMARY KEY,
    user_comment TEXT,
    publication_date timestamptz NOT NULL,
    post_id FOREIGN KEY(id) REFERENCES posts(id) ON DELETE CASCADE,
    user_id REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS post_likes(
    id  SERIAL Primary Key,
    post_id REFERENCES posts(id) ON DELETE CASCADE,
    post_like BOOLEAN
);

CREATE TABLE IF NOT EXISTS comment_likes(
    id  SERIAL Primary Key,
    comment_id REFERENCES comment(id) ON DELETE CASCADE,
    comment_like BOOLEAN
);

CREATE table IF NOT EXISTS visitors(
    id SERIAL PRIMARY KEY,
    post_id FOREIGN KEY(id) REFERENCES posts(id) ON DELETE CASCADE, 
    user_id REFERENCES users(id) ON DELETE SET NULL  
);