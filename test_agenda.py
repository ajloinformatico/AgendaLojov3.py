"""
check methods of contact Class
"""
import pytest
from agenda import *

###################################### TEST Contacto CLASS #############################


c = Contacto("Antonio", "99999999")
grupo = Grupo(Contacto("cristian", "95678887"), Contacto("Lucia", "888888888"), "Pareja")


def test_contacto():
    """
    Check constructor of the Contacto class, The real checks are done by BaseDeDatos
    class
    """
    # Check Contacto constructos
    assert Contacto("Juan", "9999999")
    contacto = Contacto("Juan", "9999999")
    assert contacto.__str__() == "Juan 9999999"

    # Check Contacto getters


def test_geters_class_contacto():
    """
    Check getters of the Contacto class
    """
    assert c.get_nombre() == "Antonio"
    assert c.nombre == "Antonio"
    assert c.get_numero() == "99999999"
    assert c.numero == "99999999"


def test_setters_class_contacto():
    """
    Check setters of the Contacto class
    """
    # before the name was Antonio
    assert c.get_nombre() == "Antonio"

    # Set name Pepito and now c.name is Pepito
    c.set_name("Pepito")
    assert c.get_nombre() == "Pepito"

    # The same with the number
    c.set_numero("956908998")
    assert c.get_numero() == "956908998"

    # setter for nombre and numero at the same time
    assert c.__str__() == "Pepito 956908998"
    c.set_contacto("Arcipreste", "89988899")
    assert c.nombre == "Arcipreste"
    assert c.numero == "89988899"
    assert c.__str__() == "Arcipreste 89988899"


################################# TEST GRUPO CLASSS ###################################################


def test_grupo():
    """
    Check constructor of group
    """
    assert Grupo(Contacto("cristian", "95678887"), Contacto("Lucia", "888888888"), "Pareja")
    # Check Contacto_origen and Contacto_miembro by getters and setters of Concat class
    assert grupo.contacto_ori.nombre == "cristian"
    assert grupo.contacto_ori.numero == "95678887"
    assert grupo.contacto_miem.nombre == "Lucia"
    assert grupo.contacto_miem.numero == "888888888"
    assert grupo.relacion == "Pareja"


def test_getters_class_grupo():
    """
    Check getters of grupo class
    """
    # get contacto_origen
    contacto_origen = grupo.get_contacto_ori()

    # getters of Contacto class
    assert contacto_origen.get_nombre() == "cristian"
    assert contacto_origen.get_numero() == "95678887"

    # get contacto_miembro
    contacto_miembro = grupo.get_contacto_miem()

    # getters of Contacto class
    assert contacto_miembro.get_nombre() == "Lucia"
    assert contacto_miembro.get_numero() == "888888888"


def test_setters_class_grupo():
    """
    Check setters of grupo class
    """
    # check contacto_origen before update
    contacto_origen = grupo.get_contacto_ori()
    assert contacto_origen.get_nombre() == "cristian"
    assert contacto_origen.get_numero() == "95678887"

    # set contacto_origen Pedro 956888844
    grupo.set_contacto_ori(Contacto("Pedro", "956888844"))

    # get contacto_origen after update by Contacto getters methods to check name and number
    contacto_origen = grupo.get_contacto_ori()
    assert contacto_origen.get_nombre() == "Pedro"
    assert contacto_origen.get_numero() == "956888844"

    # check contacto_miembro before update
    contacto_miembro = grupo.get_contacto_miem()
    assert contacto_miembro.get_nombre() == "Lucia"
    assert contacto_miembro.get_numero() == "888888888"

    # set contacto_miembro Amancio 953838864
    grupo.set_contacto_miem(Contacto("Amancio", "888888888"))

    # get contacto_origen before update by Contacto getters methods to check name and number
    contacto_miembro = grupo.get_contacto_miem()
    assert contacto_miembro.get_nombre() == "Amancio"
    assert contacto_miembro.get_numero() == "888888888"

    # check relacion before update
    assert grupo.relacion == "Pareja"

    # set relacion Mejor Amiga
    grupo.set_relacion("Mejor amiga")

    # Check relacion before update
    assert grupo.relacion == "Mejor amiga"


##################################### TEST AGENDA CLASS ########################################

def test_agenda():
    """
    Constructor and setters of Agenda
    the agenda builder creates two empty lists and the contacts and calendar
    are loaded using the setters
    """
    assert Agenda()

    # Create Agenda
    agenda = Agenda()
    agenda.set_contactos([c, Contacto("Miguel", "999555666")])
    agenda.set_grupos([grupo, Grupo(Contacto("Zahir", "898898898"), Contacto("Maria", "777888999"), "Madre")])

    # Check contact list
    contactos = agenda.get_contactos()

    # (first contact of the list)
    assert contactos[0].get_nombre() == "Arcipreste"
    assert contactos[0].get_numero() == "89988899"
    # (second contact if the list)
    assert contactos[1].get_nombre() == "Miguel"
    assert contactos[1].get_numero() == "999555666"

    # Check grupos list
    grupos = agenda.get_grupos()

    # check the types to make sure I can access the data
    assert type(grupos[0]) == Grupo
    assert type(grupos[0].contacto_ori) == Contacto
    assert type(grupos[0].contacto_miem) == Contacto
    assert type(grupos[0].relacion) == str

    # (first grupo of the list)
    assert grupos[0].contacto_ori.get_nombre() == "Pedro"
    assert grupos[0].contacto_ori.get_numero() == "956888844"
    assert grupos[0].contacto_miem.get_nombre() == "Amancio"
    assert grupos[0].contacto_miem.get_numero() == "888888888"
    assert grupos[0].relacion == "Mejor amiga"

    # (second grupo of the list)
    assert grupos[1].contacto_ori.get_nombre() == "Zahir"
    assert grupos[1].contacto_ori.get_numero() == "898898898"
    assert grupos[1].contacto_miem.get_nombre() == "Maria"
    assert grupos[1].contacto_miem.get_numero() == "777888999"
    assert grupos[1].relacion == "Madre"