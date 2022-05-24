
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name TEXT Primary Key NOT NULL,
    user_password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    birth_date DATE NOT NULL
);

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price FLOAT NOT NULL,
    publication_date DATE NOT NULL,
    user_id FOREIGN KEY REFERENCES users ON DELETE CASCADE
);

CREATE TABLE post_images(
    image_id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    image_blob,
    publication_date DATE NOT NULL,
    post_id FOREIGN KEY REFERENCES posts ON DELETE CASCADE
)

CREATE TABLE comments(
    comment_id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    publication_date DATE NOT NULL,
    post_id FOREIGN KEY REFERENCES posts ON DELETE CASCADE,
)

CREATE TABLE post_likes(
    post_id FOREIGN KEY REFERENCES posts ON DELETE CASCADE,
    post_like BOOLEAN
)

CREATE TABLE comment_likes(
    comment_id FOREIGN KEY REFERENCES posts ON DELETE CASCADE,
    comment_like BOOLEAN
)

CREATE table visitors(
    post_id FOREIGN KEY REFERENCES posts ON DELETE CASCADE,
    visitor_id TIMESTAMP
)