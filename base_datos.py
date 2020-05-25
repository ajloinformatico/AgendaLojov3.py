import pymysql
import funciones


class BaseDeDatos:
    def __init__(self, usu, passw):
        """
        Constructor of the BaseDeDatos class, check connection and then create self attr with the conexion
        and a atrr with the cusros
        Args:
            usu {str}: user string
            passw {str}: password string
        """
        if funciones.comprueba_conexion(usu, passw):
            self.conexion = pymysql.connect("localhost", usu, passw, "agendaLojo")
            self.cursor = self.conexion.cursor()
        else:
            raise ValueError("El usuario y la contraseña no son correctos")

    def get_conexion(self):
        """
        Get the connection with the database
        Returns: return the connection to the database
        """
        return self.conexion

    def close_conexion(self):
        """stop the connection with the database

        Returns connect.close(): close the connection
        """
        return self.conexion.close()

    def select(self, tabla):
        """execute and store a select

        Args:
            tabla {string}: table string  where we want to make the select
        Returns{list}: list of tuples of the rows
        """
        list_select = []  # list to save the rows
        self.cursor.execute("select * from " + tabla)
        rows = self.cursor.fetchall()  # save al the execute of cursor
        for row in rows:
            list_select.append(row)  # store in the list each row in the form of a tuple
        return list_select

    def select_filter(self, tabla, param):
        """
        execute select with filter parameter
        Args:
            tabla {string}: tabla string where we want to make the select
            param {tuple}: tuple of parameters for filter it must contains two dates 1. where to look for and 2. what to look

        Returns {list}: values of the filter select
        """
        if funciones.comprueba_tupla(param):
            list_select = []
            regex = "'%" + param[1] + "%'"
            # select * from usuario where email like '%st@%';
            self.cursor.execute("select * from " + tabla + " where " + param[0] + " like " + regex)
            rows = self.cursor.fetchall()
            for row in rows:
                list_select.append(row)
            return list_select
        else:
            raise ValueError("param must be a tuple with to args where to look for and what to look")


    def update_contacto(self, tabla, param: tuple):
        """
        Update a table of the database
        Args:
            tabla {str}: tabla string to update
            param {tuple}: dates for make the update

        Returns: update database or raise

        """
        if funciones.comprueba_tupla(param):
            self.cursor.execute(
                "update " + tabla + " set " + param[0] + " = '" + param[1] + "' where " + " nombre  = '" + param[
                    2] + "'")
            self.conexion.commit()
        else:
            raise ValueError("param must be a tuple with to args where to look for and what to look")

    def insert(self, tabla, datos: tuple):  # [param : type] is used to show a warning if tabla isn't tuple
        """insert dates into a table

        Arguments:
            tabla {string} -- name of the table
            datos {tuple} -- dates to insert into the table
        """
        # use join to convert tuple to string who contains ", %s" for each element of the tuple
        if funciones.comprueba_tupla(datos):
            args = ", ".join(("%s " * len(datos)).split())
            self.cursor.execute("insert into " + tabla + " values(" + args + ")", datos)
            self.conexion.commit()
        else:
            raise ValueError("datos must be a tuple of two params")

    def if_contain(self, param: tuple):
        """
        Check if the parameters exists
        Args:
            param tuple: tuple of the row where we want to look for and the param to look

        Returns {bool}:True  if param exits , False if not exists

        """
        self.cursor.execute("select * from " + param[0])
        for (nombre, numero) in self.cursor.fetchall():
            if param[1].lower() in nombre.lower() or param[1] in numero:
                return True
        return False

    def if_exists(self, param: tuple):
        """
        Check if param exists on the database
        Args:
            param {tuple}: uple of the row where we want to look for and the param to look

        Returns {bool}: True  if param exits , False if not exists

        """
        self.cursor.execute("select * from " + param[0])
        for (nombre, numero) in self.cursor.fetchall():
            if param[1].lower() == nombre.lower() or param[1] == numero:
                return True
        return False

    def delete_all(self):
        """delete all row of the database
        """
        self.cursor.execute("delete from contacto")
        self.cursor.execute("delete from grupos")
        self.conexion.commit()

    def get_count_grupos(self, nombre):
        """
        returns the number of contacts in which the user is a user_origin
        Args:
            nombre {str}: string of user to look for
        Returns {str}: return string format the number of groups in  which the user is a user_origin
        """
        self.cursor.execute("select count(relacion) from grupos where contacto_origen = (%s)", nombre)
        return self.cursor.fetchall()[0][0]

    def get_grupos(self, nombre):
        """
        return string group of the contact
        Args:
            nombre {str}: string of user to look for

        Returns {str}:  return string format the group in  which the user is a user_origin or user_member

        """
        self.cursor.execute(
            "select relacion from grupos where contacto_origen = (%s) or contacto_miembro = (%s)",
            (nombre, nombre))
        return self.cursor.fetchall()[0][0]

    def initial_insert(self):
        """Insert example dates to the database for begin the gui main
        """
        self.delete_all()  # before insert delete all
        self.cursor.execute("insert into contacto values (%s, %s)", ("Pedro", "956787889"))
        self.cursor.execute("insert into contacto values (%s, %s)", ("Juan", "956757575"))
        self.cursor.execute("insert into contacto values (%s, %s)", ("Patricia", "678876678"))
        self.cursor.execute("insert into contacto values (%s, %s)", ("Pepe", "787777777"))
        self.cursor.execute("insert into contacto values (%s, %s)", ("Cristian", "345533553"))
        self.cursor.execute("insert into contacto values (%s, %s)", ("Maria", "233223322"))
        self.cursor.execute("insert into contacto values (%s, %s)", ("Elena", "898898898"))
        self.cursor.execute("insert into contacto values (%s, %s)", ("Juaquin", "899899899"))
        self.conexion.commit()
        self.cursor.execute("insert into grupos values (%s, %s, %s)", ("Pedro", "Juan", "familia"))
        self.cursor.execute("insert into grupos values (%s, %s, %s)", ("Patricia", "Pepe", "pareja"))
        self.cursor.execute("insert into grupos values (%s, %s, %s)", ("Cristian", "Maria", "amistad"))
        self.cursor.execute("insert into grupos values (%s, %s, %s)", ("Elena", "Juaquin", "trabajo"))
        self.cursor.execute("insert into grupos values (%s, %s, %s)", ("Cristian", "Juaquin", "Vecinos"))
        self.conexion.commit()

    def delete_filter(self, param: tuple):
        """
        execute a delete where param[0] == Table, param[1] == column, param[2] == child
        Args:
            param {tuple}: values to delete

        Returns void: delete from database
        """
        print(param[0], param[1], param[2])
        self.cursor.execute("delete from " + param[0] + " where " + param[1] + " like '%" + param[2] + "%'")
        self.conexion.commit()


if __name__ == "__main__":
    pass
    ### Test de la clase en main
    ### Prueba instancia de la base de datos
    bd = BaseDeDatos("pepito", "grillo")
    # bd = BaseDeDatos("manuel", "gonzalez")
    ### Prueba funcion inserccion inicial y delete_all
    bd.initial_insert()
    ### Prueba select simple
    # print(bd.select("contacto"))
    # print(bd.select("grupos"))
    ### Prueba select_filter
    # print(bd.select_filter("contacto", ("nombre", "pepe")))

    ### Pureba método insert
    # bd.insert("contacto", ("Miguel", "999999999"))
    # print(bd.select_filter("contacto", ("nombre", "juan")))

    ### Prueba método if exists
    # print(bd.if_exists(("contacto", "Pepe")))

    ### Ptueba método if_contains
    # print(bd.if_exists(("contacto", "Pepe")))

    ### Prueba  método get_count_grupos():
    # print(bd.get_count_grupos("manuela")) # devuelve cero
    # print(bd.get_count_grupos("cristian")) # devuelve dos

    ### Pureba método update_contacto
    # print(bd.select("Grupos"))  # Before make update
    # bd.update_contacto("contacto", ("nombre", "Manuela", "Cristian"))
    # bd.update_contacto("contacto", ("numero", "999999999", "Elena"))
    # print(bd.select("Grupos"))  # After make update

    ### Prueba Get_grupos
    # print(bd.get_grupos("Cristian"))