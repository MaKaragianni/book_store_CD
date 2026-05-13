CREATE TABLE IF NOT EXISTS films (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  director VARCHAR(255)
);

TRUNCATE TABLE films RESTART IDENTITY CASCADE;

INSERT INTO films (title, director)
VALUES ('Mortal Kombat II', 'Simon McQuoid');

INSERT INTO films (title, director)
VALUES ('The Devil Wears Prada 2', 'David Frankel');

INSERT INTO films (title, director)
VALUES ('Oppenheimer', 'Christopher Nolan');

INSERT INTO films (title, director)
VALUES ('Project Hail Mary', 'Phil Lord');