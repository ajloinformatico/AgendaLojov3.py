import pymysql


def comprueba_conexion(usu, passw):
    """
    function to check connection to the database
    Args:
       usu {str}: user string
       passw {str}: password string

    Returns {bool}: True if connects, False if not connect
    """
    try:
        pymysql.connect("localhost", usu, passw, "agendaLojo")
        return True
    except pymysql.err.OperationalError:  # error de conexion
        return False
    except RuntimeError:  # error en la contraseña
        return False


def comprueba_tupla(param):
    """
    Function to check if param type is tuple
    Args:
        param {tuple}:

    Returns {bool}: True tuple with length of 2, None just tuple, False isnt tuple
    """
    if isinstance(param, tuple):
        return True
    return False




def comprueba_numero(param):
    """
    Check if param is a telephnone number
    Args:
        param {str}:

    Returns {bool}: True if its a number, False if its not a number

    """
    if 10 >= len(param) >= 6:
        try:
            int(param)
            return True
        except ValueError:
            return False
    return False
