DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS user;

CREATE TABLE category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_id INTEGER NOT NULL,
  name TEXT UNIQUE NOT NULL,
  unit_price INTEGER NOT NULL,
  discount INTEGER NOT NULL,
  FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

INSERT INTO user (username, password, role)
VALUES (
        'admin',
        'pbkdf2:sha256:260000$VYDGNEBpIGepNUIm$5dee1a7ed6c68cdd42f0c80005341468aebc801a29bbfe1906b74f3abf8adcf0',
        'ADMIN'
);