USE db_pokemon;

 CREATE TABLE pokemon(
     id INTEGER,
     name varchar(20) PRIMARY KEY,
     height INTEGER,
     weight INTEGER
 );
 CREATE TABLE owner(
     name varchar(20) PRIMARY KEY,
     town varchar(20)
 );
 create table ownedBy(
     pokemon_name VARCHAR(20),
     FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
     owner_name VARCHAR(20),
     FOREIGN KEY (owner_name) REFERENCES owner(name)
 );
 create table types(
     pokemon_name VARCHAR(20),
     FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
     pokemon_type varchar(20)
 );

