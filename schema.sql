
CREATE TABLE IF NOT EXISTS user(
    id SERIAL Primary Key,
    username TEXT Unique NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    birth_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS post(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    publication_date timestamptz,
    user_id REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS post_image(
    id SERIAL PRIMARY KEY,
    image_name TEXT NOT NULL Unique,
    publication_date timestamptz,
    post_id REFERENCES posts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comment(
    id SERIAL PRIMARY KEY,
    user_comment TEXT,
    publication_date timestamptz NOT NULL,
    post_id FOREIGN KEY(id) REFERENCES posts(id) ON DELETE CASCADE,
    user_id REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS post_like(
    id  SERIAL Primary Key,
    post_id REFERENCES posts(id) ON DELETE CASCADE,
    post_like BOOLEAN
);

CREATE TABLE IF NOT EXISTS comment_like(
    id  SERIAL Primary Key,
    comment_id REFERENCES comment(id) ON DELETE CASCADE,
    comment_like BOOLEAN
);

CREATE table IF NOT EXISTS visitor(
    id SERIAL PRIMARY KEY,
    post_id FOREIGN KEY(id) REFERENCES posts(id) ON DELETE CASCADE, 
    user_id REFERENCES users(id) ON DELETE SET NULL  
);