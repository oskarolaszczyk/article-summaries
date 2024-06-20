CREATE TYPE UserType AS ENUM ('ADMIN', 'USER');
CREATE TYPE ModelType AS ENUM ('MEANINGCLOUD', 'OUR_MODEL');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(320) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    type UserType NOT NULL DEFAULT 'USER',
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    title VARCHAR(200) NOT NULL,
    source_url VARCHAR NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE summaries (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id) NOT NULL,
    content TEXT NOT NULL,
    rating BOOLEAN,
    model_type ModelType NOT NULL,
    date_generated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users(username, email, password, type) VALUES
    ('admin', 'admin@example.com', '$2b$12$U7rOuUQ.Xh0TZtQHDuqbT.sCfQxtLn2BJDJHMdbSXlTIMla.VqLfC', 'ADMIN'),
    ('test', 'test@example.com', '$2b$12$xoOCld0dN/Qjb6IJ4/AhseaTe/dPMNW7fSvXTEbXa5.nqtccs2cbq', 'USER'),
    ('test2', 'test2@example.com', '$2b$12$xoOCld0dN/Qjb6IJ4/AhseaTe/dPMNW7fSvXTEbXa5.nqtccs2cbq', 'USER');
