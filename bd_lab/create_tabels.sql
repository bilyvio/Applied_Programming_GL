CREATE TABLE category (
    uid SERIAL NOT NULL,
    name VARCHAR ,
    homePage VARCHAR ,
    PRIMARY KEY (uid)
);

CREATE TABLE announcement (
    uid SERIAL NOT NULL,
    name VARCHAR ,
    releaseDate VARCHAR,
    local INTEGER,
    manufacturer INTEGER ,
    PRIMARY KEY (uid),
    FOREIGN KEY(manufacturer) REFERENCES category (uid)
);

CREATE TABLE users (
    uid SERIAL NOT NULL,
    name VARCHAR ,
    PRIMARY KEY (uid)
);