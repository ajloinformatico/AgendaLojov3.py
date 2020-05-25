"""
Check extra methods for the Agenda
"""
from funciones import *
import pytest


def test_comprueba_conexion():
    """
    The user of the agenda is pepito grillo (agendaLojo.sql)
    checks if he can only access the

    Returns {bool}: True execute pymysql.connect False, Warning
    """
    assert comprueba_conexion("Juanito", "Macande") == False

    # Only him can acces to Agenda
    assert comprueba_conexion("pepito", "grillo") == True


def test_tupla():
    """
    Check if the parameter is tuple this has been used to force the typing in
    the application
    by repeating both I decided to put it as an extra method
    Returns {bool}: True for tuple type, False for another Type
    """
    assert comprueba_tupla("contacto") == False
    assert comprueba_tupla(("contacto", "Pepe")) == True
    assert comprueba_tupla((2, "jjj")) == True


def test_comprueba_numero():
    """
    Check if param is a numeric format and the length of the number is between 10 and 6
    its used to checl Telephones Number
    Returns {bool}: True for number with length beetween 10 and 6 False for another type
    """
    assert comprueba_numero(999) == False
    assert comprueba_numero("98989898") == True
    assert comprueba_numero([9, 6, 5, 4, 5, 4]) == False
    assert comprueba_numero("dfdfdf") == False
    assert comprueba_numero("89888888888888888") == False
    assert comprueba_numero(878878878) == True
