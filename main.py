import funciones  # libreria de funciones extra
from base_datos import BaseDeDatos
from agenda import Agenda, Contacto, Grupo
from gui_grupos import Gui_grupos
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk

import sys


class Login:

    def __init__(self):
        """Constructor of the gui
        """
        self.gui_login = tk.Tk()
        self.gui_login.title("Agenda_Lojo v2.0")
        self.load_widgets_login()
        self.gui_login.mainloop()

    def login(self):
        """
        Check if user exist in the database and load Principal gui with the connection to the database
        Returns {bool}: True Load Gui Principal and database, False return warning

        """
        if funciones.comprueba_conexion(self.input_usuario.get(), self.input_contrasena.get()):

            bd = BaseDeDatos(self.input_usuario.get(), self.input_contrasena.get())
            bd.initial_insert()
            self.gui_login.destroy()
            Principal(bd)
            # call main gui with the connection
            return True
        else:
            messagebox.showwarning("Error", "Usuario o contraseña incorrectos")
            return False

    def login_salir(self):
        """
        close the window and finish the program
        Returns void: close the gui and make sys.exit()
        """
        self.gui_login.destroy()
        sys.exit()

    def load_widgets_login(self):
        """load widgets of the Login Gui
        """
        # l1.grid(row=0, column=0, padx=(100, 10)) izq derc
        #  l2.grid(row=1, column=0, pady=(10, 100)) arriba abajo
        self.txt_usuario = tk.Label(self.gui_login, text="Introduzca su nombre")
        self.txt_usuario.grid(column=0, row=0, columnspan=2, pady=(10, 5))

        self.input_usuario = tk.Entry(self.gui_login, width=30)
        self.input_usuario.grid(column=0, row=1, columnspan=2, padx=20)

        self.txt_contrasena = tk.Label(self.gui_login, text="Introduzca su contraseña")
        self.txt_contrasena.grid(column=0, row=2, columnspan=2, pady=(20, 5))

        self.input_contrasena = tk.Entry(self.gui_login, show="*", width=30)
        self.input_contrasena.grid(column=0, row=3, columnspan=2, padx=20)

        self.btn_login = tk.Button(self.gui_login, text="Login", width="12", height="2",
                                   command=self.login)
        self.btn_login.grid(column=0, row=4, pady=(15, 10), padx=20)

        self.btn_salir = tk.Button(self.gui_login, text="Salir", width="12", height="2",
                                   command=self.login_salir)
        self.btn_salir.grid(column=1, row=4, pady=(15, 10), padx=20)


class Principal:
    """Clase de la interfaz principal de la aplicación
    """

    def __init__(self, bd):
        """constructor of the main gui

        Arguments:
            nombre {string} -- name of the database user
            contrasena {string} -- name of the database
        """
        self.gui_principal = tk.Tk()
        self.gui_principal.title("Agenda Lojo v2.0")
        self.bd = bd
        self.agenda = Agenda()  # Load empty agenda object
        self.load_data()  # load dates for agenda objects
        self.gui_principal.geometry("600x400")
        self.load_widgets_principal()
        self.gui_principal.mainloop()

    ################################## Datos ##########################################################

    def load_data(self):
        """call funcion load_agenda from agenda.Agenda and load dates of the agenda objects from select statements
        """
        self.agenda.load_agenda(self.bd.select("contacto"), self.bd.select("grupos"))
        print(self.agenda)

    def load_data_treeview(self):
        ### Hacer con una consulta en la clase
        """
        select c.nombre g.nombre (select distinct(cpnir) where mose)
        """
        for contacto in self.agenda.contactos:
            datos = self.agenda.get_contacto_numero_grupo(contacto)
            num_grupo = self.bd.get_count_grupos(contacto.nombre)
            self.consulta_pri.insert("", tk.END, text=datos[0], value=(datos[1], num_grupo))

    def load_data_treeview_after_update(self):
        for contacto in self.agenda.contactos:
            num_grupo = self.bd.get_count_grupos(contacto.nombre)
            if self.input_busca.get().lower() in contacto.nombre.lower() or self.input_busca.get().lower() in contacto.numero.lower():
                # I use this condition simply to discriminate when inserting to Treeview
                self.consulta_pri.insert("", tk.END, text=contacto.nombre, values=(contacto.numero, num_grupo))

    def load_Treeview_consulta_pri(self):
        """load treeview table
        """
        # crea el treeview con los nombres de las columnas
        self.consulta_pri = ttk.Treeview(self.gui_principal, columns=("telefono", "grupo"))
        # los nombres de las columnas se utilizan como índices, #0 se utiliza como indice la primera
        self.consulta_pri.heading("#0", text="Nombre")
        self.consulta_pri.heading("telefono", text="Telefono")
        self.consulta_pri.heading("grupo", text="Nº contactos grupo")
        self.consulta_pri.grid(column=0, row=1, columnspan=6, pady=20)
        # para hacer el scroll hay que icnorporar ttk.Scrollbar, colocarlo, configurar el Treeview despues
        # Tiene que ser en ese orden si no no funcion
        self.vsb = ttk.Scrollbar(self.gui_principal, orient="vertical", command=self.consulta_pri.yview)
        self.vsb.grid(column=5, row=1, sticky="nse")
        self.consulta_pri.configure(yscrollcommand=self.vsb.set)

    ############################################ Busca ################################################

    def busca(self):
        """
        Search from a parameter the matching contacts use the methods Database
        if_exists() and get_count_grupos()
        Returns void: insert into Treeview the contacto.nombre, contacto.numero and num_grupo
        """
        self.load_Treeview_consulta_pri()  # primero vacia el treeview
        if self.bd.if_contain(("contacto", self.input_busca.get())):
            self.load_data_treeview_after_update()
        else:
            self.consulta_pri.insert("", tk.END, text="null", values=("null", "null"))

    ##################################### Añade Contacto #########################################################

    def anade_contacto(self):
        """
        call the secondary dialog to add a new contact
        Returns {void}: new child gui of gui_principal to add new contact

        """
        self.gui_anadir = tk.Toplevel(self.gui_principal)
        self.gui_anadir.title("Agenda Lojo v2.0")
        self.load_anadir_gui()
        self.gui_anadir.mainloop()

    def gui_anadir_register(self):
        """
        method use for child gui_anadir to register new contact
        Returns {Void} :
        insert the data into the database and contacts
        """
        if self.imput_new_user.get != "" and self.input_new_number.get() != "":
            if funciones.comprueba_numero(self.input_new_number.get()):
                if not self.bd.if_exists(("contacto", self.imput_new_user.get())) and not self.bd.if_exists(
                        ("contacto", self.input_new_number.get())):
                    self.bd.insert("contacto", (self.imput_new_user.get(), self.input_new_number.get()))
                    contacto = Contacto(self.imput_new_user.get(), self.input_new_number.get())
                    self.agenda.add_contacto(contacto)
                    self.load_Treeview_consulta_pri()
                    self.load_data_treeview_after_update()
                    self.gui_anadir_salir()
                else:
                    messagebox.showwarning("Error", "Los datos ya existen en la agenda")
            else:
                messagebox.showwarning("Error", "El número no es valido")
        else:
            messagebox.showwarning("Error", "Campos vacíos")

    def gui_anadir_salir(self):
        """
        close gui_anadir child gui
        Returns {void}: close the child gui

        """
        self.gui_anadir.withdraw()

    ############################################## Edita Contacto ###############################################

    def edita_contacto(self):
        """
        call the secondary dialog to edit a contact checking if the selection is valid

        Returns {void}: new child gui of gui_principal to edit new contact or warning if check fail
        """
        indice = self.consulta_pri.focus()
        self.usu = self.consulta_pri.item(indice)['text']
        if self.usu != "null" and self.usu != "":
            self.gui_edita_contacto = tk.Toplevel(self.gui_principal)
            self.gui_edita_contacto.title("Agenda Lojo v2.0")
            self.load_edita_contacto_gui()  # widgets for edita_contacto
            self.gui_edita_contacto.mainloop()
        else:
            messagebox.showwarning("Alerta", "No has seleccionado ningun contacto")

    def gui_edita_contacto_modifica(self):
        """
        after checking the entry run an update and reload the application data
        Returns {void}: after update reload aplication load

        """
        print(self.usu)
        if self.imput_edit_user.get() != "" and self.input_edit_number.get():
            if funciones.comprueba_numero(self.input_edit_number.get()):
                if not self.bd.if_exists(("contacto", self.imput_edit_user.get())) and not self.bd.if_exists(
                        ("contacto", self.input_edit_number.get())):
                    ask = messagebox.askyesno("Alerta", "Estás seguro de que quieres modificar a " + self.usu)
                    if ask:
                        self.bd.update_contacto("contacto", ("numero", self.input_edit_number.get(), self.usu))
                        self.bd.update_contacto("contacto", ("nombre", self.imput_edit_user.get(), self.usu))
                        self.bd.cursor.execute("update grupos set contacto_origen = '%s' where contacto_origen like "
                                               "'%s'"  % (self.imput_edit_user.get(), self.usu))
                        self.bd.conexion.commit()
                        self.bd.cursor.execute("update grupos set contacto_miembro = '%s' where contacto_miembro like "
                                               "'%s'"  % (self.imput_edit_user.get(), self.usu))

                        # self.bd.conexion.commit()
                        self.agenda = Agenda()
                        self.load_data()
                        self.load_Treeview_consulta_pri()
                        self.load_data_treeview_after_update()
                        self.gui_edita_contacto_salir()

                else:
                    messagebox.showwarning("Error", "Datos ya existen en la agenda")
            else:
                messagebox.showwarning("Error", "El teléfono no es válido")
        else:
            messagebox.showwarning("Error", "Campos vacíos")

    def gui_edita_contacto_salir(self):
        self.gui_edita_contacto.withdraw()

    ################################ Elimina el contacto #######################################################

    def elimina_contacto(self):
        """
        delete contacto from angeda.contactos and bd
        Returns void: delete if contacto != "None", else show warning
        """
        indice = self.consulta_pri.focus()  # get indix
        usu = self.consulta_pri.item(indice)['text']  # query_pri () works like a dictionary with the index we get
        # the value of the text key which is the user's string
        print(usu)
        if usu != "null" and usu != "":
            ask = messagebox.askyesno("Alerta", "Estas seguro de que quiere eliminar a " + usu)
            if ask:
                self.agenda.remove_contacto(usu)  # delete contacto from agenda.contactos
                self.bd.delete_filter(("grupos", "contacto_origen", usu))  # delete grupo from bd
                self.bd.delete_filter(("contacto", "nombre", usu))  # delete contacto from bd

                self.load_Treeview_consulta_pri()
                self.load_data_treeview_after_update()
        else:
            messagebox.showwarning("Alerta", "No has seleccionado ningun contacto")

    #################################### Gestion Grupos ########################################################

    def ventana_grupo(self):

        Gui_grupos(self.bd, self.agenda, self.consulta_pri, self.gui_principal)
        self.agenda = Agenda()

    ############################################# Exit ############################################################

    def principal_salir(self):
        """
        close Principal gui and exit the program
        Returns vois: exit the program

        """
        self.gui_principal.destroy()
        sys.exit()

    ################################################ Widgets #########################################################

    def load_widgets_principal(self):
        """load all the widgets of the Principal gui
        """
        self.input_busca = tk.Entry(self.gui_principal, width="47")
        self.input_busca.grid(column=0, row=0, columnspan=5, pady=(10, 5), padx=(15, 0))

        self.btn_busca = tk.Button(self.gui_principal, text="Buscar", width="12", height="2",
                                   command=self.busca)
        self.btn_busca.grid(column=5, row=0, pady=(10, 5), padx=(0, 15))

        self.load_Treeview_consulta_pri()
        self.load_data_treeview()

        # botones del final
        self.btn_anadir = tk.Button(self.gui_principal, text="Añadir", width="10", height="2",
                                    command=self.anade_contacto)
        self.btn_anadir.grid(column=0, row=2, padx=(15, 0))

        self.btn_editar = tk.Button(self.gui_principal, text="Editar", width="10", height="2",
                                    command=self.edita_contacto)
        self.btn_editar.grid(column=1, row=2)

        self.btn_eliminar = tk.Button(self.gui_principal, text="Eliminar", width="10", height="2",
                                      command=self.elimina_contacto)
        self.btn_eliminar.grid(column=2, row=2)

        self.btn_grupo = tk.Button(self.gui_principal, text="Grupo", width="10", height="2",
                                   command=self.ventana_grupo)
        self.btn_grupo.grid(column=3, row=2)

        self.btn_salir = tk.Button(self.gui_principal, text="Salir", width="10", height="2",
                                   command=self.principal_salir)  # Cierra el programa
        self.btn_salir.grid(column=5, row=2, padx=(0, 15))

    def load_anadir_gui(self):
        """
        Load widgets of child gui anadir_gui
        """
        self.txt_new_user = tk.Label(self.gui_anadir, text="Introduzca el nombre")
        self.txt_new_user.grid(column=0, row=0, columnspan=2, pady=(10, 5))

        self.imput_new_user = tk.Entry(self.gui_anadir, width=30)
        self.imput_new_user.grid(column=0, row=1, columnspan=2, padx=20)

        self.txt_new_number = tk.Label(self.gui_anadir, text="Introduzca un numero")
        self.txt_new_number.grid(column=0, row=2, columnspan=2, pady=(20, 5))

        self.input_new_number = tk.Entry(self.gui_anadir, width=30)
        self.input_new_number.grid(column=0, row=3, columnspan=2, padx=20)

        self.btn_register = tk.Button(self.gui_anadir, text="Registrar", width="12", height="2",
                                      command=self.gui_anadir_register)
        self.btn_register.grid(column=0, row=4, pady=(15, 10), padx=20)

        self.btn_salir = tk.Button(self.gui_anadir, text="Cerrar", width="12", height="2",
                                   command=self.gui_anadir_salir)
        self.btn_salir.grid(column=1, row=4, pady=(15, 10), padx=20)

    def load_edita_contacto_gui(self):
        """
        Load widgets of child gui anadir_gui
        """

        self.txt_edit_user = tk.Label(self.gui_edita_contacto, text="Introduzca un nuevo nombre nombre")
        self.txt_edit_user.grid(column=0, row=0, columnspan=2, pady=(10, 5))

        self.imput_edit_user = tk.Entry(self.gui_edita_contacto, width=30)
        self.imput_edit_user.grid(column=0, row=1, columnspan=2, padx=20)

        self.txt_edit_number = tk.Label(self.gui_edita_contacto, text="Introduzca un nuevo numero")
        self.txt_edit_number.grid(column=0, row=2, columnspan=2, pady=(20, 5))

        self.input_edit_number = tk.Entry(self.gui_edita_contacto, width=30)
        self.input_edit_number.grid(column=0, row=3, columnspan=2, padx=20)

        self.btn_edita = tk.Button(self.gui_edita_contacto, text="Modificar", width="12", height="2",
                                   command=self.gui_edita_contacto_modifica)
        self.btn_edita.grid(column=0, row=4, pady=(15, 10), padx=20)

        self.btn_salir_edita = tk.Button(self.gui_edita_contacto, text="Cerrar", width="12", height="2",
                                         command=self.gui_edita_contacto_salir)
        self.btn_salir_edita.grid(column=1, row=4, pady=(15, 10), padx=20)


if __name__ == "__main__":
    ### Prueba la clase login
    Login()  # The Login class is loaded with usurname and password
    ### Prueba la clase Gui
    # Principal(BaseDeDatos("pepito", "grillo"))
