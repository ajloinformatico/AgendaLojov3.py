drop database if exists agendaLojo;
create database agendaLojo;
use agendaLojo;

drop table if exists contacto;
create table contacto(
    nombre varchar(40),
    numero varchar(10) unique not null,
    constraint contacto_pk primary key(nombre)
);
drop table if exists grupos;
create table grupos(
    contacto_origen varchar(40),
    contacto_miembro varchar(40),
    relacion varchar(20) unique not null,
    constraint grup_pk primary key(contacto_origen, contacto_miembro),
    constraint c_origen_fk foreign key(contacto_origen) references contacto(nombre) ON DELETE CASCADE ON update cascade,
    constraint c_miembro_fk foreign key(contacto_miembro) references contacto(nombre) ON DELETE CASCADE ON update CASCADE
);

-- Usuario que utilizo user: pepito pass:grillo

drop user if exists 'pepito'@'localhost';
create user 'pepito'@'localhost' identified by 'grillo';
grant all privileges on * . * to 'pepito'@'localhost';
flush privileges;