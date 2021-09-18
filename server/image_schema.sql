DROP TABLE IF EXISTS images;

CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    userid INTEGER NOT NULL,
    image_name text NOT NULL,
    image_type text NOT NULL,
    image_blob BLOB NOT NULL
);