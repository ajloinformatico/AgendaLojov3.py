"""
Test for BaseDeDatos
the connection is tested through the extra functions
"""
import pytest
from base_datos import *

bd = BaseDeDatos("pepito", "grillo")


def test_get_conexion():
    """
    Check method get_conexion(). if it returns bd.conexion and the if type is pymysql.connections.Connection
    """
    assert type(bd.get_conexion()) == pymysql.connections.Connection
    assert bd.get_conexion() == bd.conexion


def test_initial_insert():
    """
    Make default insert into bd it must insert 8 contacts and 5 groups.
    It Will be checked using rowcount () function of the BaseDeDatos class
    """
    bd.initial_insert()

    bd.cursor.execute("select * from contacto")
    assert bd.cursor.rowcount == 8

    bd.cursor.execute("select * from grupos")
    assert bd.cursor.rowcount == 5


def test_select():
    """Test simple select
    """
    # check if simple select in contacto returns list of tuple with contactos
    assert bd.select("contacto") == [('Maria', '233223322'), ('Cristian', '345533553'), ('Patricia', '678876678'),
                                     ('Pepe', '787777777'), ('Elena', '898898898'), ('Juaquin', '899899899'),
                                     ('Juan', '956757575'), ('Pedro', '956787889')]

    # check if simple assert in Grupo returns list of tuple with Grupos
    assert bd.select("grupos") == [('Cristian', 'Maria', 'amistad'), ('Pedro', 'Juan', 'familia'),
                                   ('Patricia', 'Pepe', 'pareja'), ('Elena', 'Juaquin', 'trabajo'),
                                   ('Cristian', 'Juaquin', 'Vecinos')]


def test_select_filter():
    """
    Test select filter
    """
    # assert if select_filter of Pepe returns a tuple of Pepe and his number
    assert bd.select_filter("contacto", ("nombre", "pepe")) == [('Pepe', '787777777')]
    assert bd.select_filter("contacto", ("numero", "787777777")) == [('Pepe', '787777777')]

    # assert if select_filter of Juan returns a tupla of Juan and his number
    assert bd.select_filter("contacto", ("nombre", "juan")) == [('Juan', '956757575')]
    assert bd.select_filter("contacto", ("numero", "956757575")) == [('Juan', '956757575')]


def test_update_contacto():
    """
    check if after update Pepe to Juan if we make a select of Pepe it will returns None but
    returns new update contact
    """
    bd.update_contacto("contacto", ("nombre", "fabio", "Pepe"))
    assert bd.select_filter("contacto", ("nombre", "pepe")) == []
    assert bd.select_filter("contacto", ("nombre", "fabio")) == [('fabio', '787777777')]

    # the same with juan
    bd.update_contacto("contacto", ("nombre", "Federico", "Juan"))
    assert bd.select_filter("contacto", ("nombre", "Juan")) == []
    assert bd.select_filter("contacto", ("nombre", "Federico")) == [('Federico', '956757575')]


def test_insert():
    """
    check if inserting contacto and grupo
    """
    bd.insert("contacto", ("Matias", "999444499"))
    bd.insert("contacto", ("Miranda", "666666666"))
    bd.insert("grupos", ("Matias", "Miranda", "Prima"))

    assert bd.select_filter("contacto", ("nombre", "Matias")) == [('Matias', '999444499')]
    assert bd.select_filter("contacto", ("nombre", "Miranda")) == [('Miranda', '666666666')]
    assert bd.select_filter("grupos", ("relacion", "Prima")) == [('Matias', 'Miranda', 'Prima')]


def test_if_contains():
    """
    Check if a table contain the param
    """
    # Pepe contains p
    assert bd.if_contain(("contacto", "p")) == True
    # there isnt contact with z
    assert bd.if_contain(("contacto", "z")) == False


def test_if_exists():
    """
    Check if number or nombre is in database
    """
    # Matias is in the database
    assert bd.if_exists(("contacto", "Matias")) == True
    # 666666666 is in the database
    assert bd.if_exists(("contacto", "666666666")) == True

    # Ronaldo isnt in the database
    assert bd.if_exists(("contacto", "Ronaldo")) == False
    assert bd.if_exists(("contacto", "33333333")) == False


def test_get_count_grupos():
    """
    Check the number of group that have an origin_concat
    """
    bd.initial_insert()
    assert bd.get_count_grupos("Cristian") == 2
    assert bd.get_count_grupos("Patricia") == 1
    assert bd.get_count_grupos("Pepe") == 0


def test_get_grupos():
    """
    check if it returns the name of the realcion from a contact
    """
    assert bd.get_grupos("Cristian") == "amistad"
    assert bd.get_grupos("Patricia") == "pareja"
    assert bd.get_grupos("Elena") == "trabajo"


def test_delete_filter():
    """
    assert delete by param
    """
    # delete from contacto where nombre == Elena
    # delete from Grupo where relacion == trabajo
    bd.delete_filter(("contacto", "nombre", "Elena"))
    bd.delete_filter(("Grupos", "relacion", "trabajo"))

    assert bd.if_exists(("contacto", "Elena")) == False


def test_close_conection():
    """
    Check if lose() return None
    """
    assert bd.conexion.close() is None
