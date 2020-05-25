use agendaLojo;
delete from grupos;
delete from contacto;


insert into contacto
values("Pedro","956787889"),
    ("Juan","956757575"),
    ("Patricia","678876678"),
    ("Pepe","787777777"),
    ("Cristian","345533553"),
    ("Maria","233223322"),
    ("Elena","898898898"),
    ("Juaquin","899899899");

insert into grupos
	values("Pedro","Juan","familia"),
		("Patricia","Pepe","pareja"),
        ("Cristian","Maria","amistad"),
        ("Elena","Juaquin","trabajo"),
        ("Cristian","Juaquin","vecinos")
