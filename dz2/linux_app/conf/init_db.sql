create database if not exists application;
use application;
create table users (username varchar(255), password varchar(255));
insert into users VALUES ("admin", "adminpass");
create user 'username'@'localhost' identified by 'password';
grant all privileges on application.* to 'username'@'localhots';
flush privileges;
