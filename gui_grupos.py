# TODO Comentar funciones cargar en el treeview los datos
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class Gui_grupos:
    """
    Load child gui for grupos in a diferent class
    """

    def __init__(self, bd, agenda, consulta_pri, gui_principal, ):
        self.bd = bd
        self.agenda = agenda
        self.consulta_pri = consulta_pri
        self.gui_principal = gui_principal
        self.gui_grupos = tk.Toplevel(gui_principal)
        self.gui_grupos.title("Agenda Lojo v2.0")
        self.load_gui_grupos_widgets()
        self.gui_grupos.mainloop()

    ########################################## Data ################################################

    def load_Treeview_consulta_gru(self):
        """
        New Treeview object to show groups
        Returns {void}: Load an empty Treeview into gui_grupos to show groups

        """
        self.consulta_gru = ttk.Treeview(self.gui_grupos, columns=("contacto_miembro", "grupo"))
        self.consulta_gru.heading("#0", text="Contacto Origen")
        self.consulta_gru.heading("contacto_miembro", text="Contacto Miembro")
        self.consulta_gru.heading("grupo", text="Grupo")
        self.consulta_gru.grid(column=0, row=1, columnspan=3, pady=10)
        self.vsb_gru = ttk.Scrollbar(self.gui_grupos, orient="vertical", command=self.consulta_gru.yview)
        self.vsb_gru.grid(column=2, row=1, sticky="nse")

    def load_treeview_consulta_gru_data(self):
        """
        Load data to the treeview from the database
        returns {void}: data to Treeview
        """
        datos = self.bd.select("grupos")
        for relacion in datos:
            self.consulta_gru.insert("", tk.END, text=relacion[0], values=(relacion[1], relacion[2]))

    def get_index_from_consulta_gru(self):
        """
        from focus on treeview you get an index and using this index as a dictionary you get the value of the text field
        Returns {str}: contacto.name of Contacto_origen

        """
        indice = self.consulta_gru.focus()  # get indix
        contacto_origen = self.consulta_gru.item(indice)['text']
        contacto_miembro = self.consulta_gru.item(indice)['values'][0]
        relacion = self.consulta_gru.item(indice)['values'][1]
        return [contacto_origen, contacto_miembro, relacion]

    ######################################## Inserta Grupo ##########################################

    def anade_gru(self):
        """
        Load a secondary dialog to add new groups
        Returns {void}: New child gui

        """
        self.anade_gru_grui = tk.Toplevel(self.gui_grupos)
        self.anade_gru_grui.title("Agenda Lojo v2.0")
        self.load_anade_gru_gui()
        self.anade_gru_grui.mainloop()

    def anade_gru_grui_insert(self):
        """
        Check that the entry is not empty and mysql exceptions to insert a new group
        Returns {void}: Insert new contact

        """
        if self.input_new_cont_origen.get() != "" and self.input_new_cont_miembro.get() != "" and self.input_new_rel.get() != "":
            try:
                self.bd.insert("grupos", (
                    self.input_new_cont_origen.get(), self.input_new_cont_miembro.get(), self.input_new_rel.get()))
                self.load_Treeview_consulta_gru()
                self.load_treeview_consulta_gru_data()
                self.anade_gru_grui_cerrar()
            except:
                messagebox.showwarning("Alerta", "Datos Erroneos")

        else:
            messagebox.showwarning("Alerta", "Campos vacíos")

    def anade_gru_grui_cerrar(self):
        """
        close child window to insert group
        Returns {void}: close child guy
        """
        self.anade_gru_grui.withdraw()

    ####################################### Edita Grupo ###########################################

    def edita_gru(self):
        try:
            self.name_grupo = self.get_index_from_consulta_gru()[2]
            self.edita_gru_gui = tk.Toplevel(self.gui_grupos)
            self.load_edita_gru_gui()
            self.edita_gru_gui.mainloop()
        except IndexError:
            messagebox.showwarning("Alerta", "No has seleccionado ningin contacto")

    def mod_gru(self):
        if self.input_edit_cont_origen.get() != "" and self.input_edit_cont_miembro.get() != "" and self.input_edit_rel.get() != "":
            try:
                self.bd.delete_filter(("grupos", "relacion", self.name_grupo))
                self.bd.insert("grupos", (
                    self.input_edit_cont_origen.get(), self.input_edit_cont_miembro.get(), self.input_edit_rel.get()))
                self.load_Treeview_consulta_gru()
                self.load_treeview_consulta_gru_data()
                self.close_edita_gru_gui()

            except:
                messagebox.showwarning("Alerta", "datos erroneos")
        else:
            messagebox.showwarning("Alerta", "Campos Vacíos")

    def close_edita_gru_gui(self):
        self.edita_gru_gui.withdraw()

    ######################################## Salir #################################################

    def elimina_gru(self):
        """
        Check that the selection is not empty and mysql exceptions to delete a group
        Returns void {void}: delete a group
        """
        try:
            grupo = self.get_index_from_consulta_gru()[2]
            ask = messagebox.askyesno("Alerta", "Estas seguro de que desea eliminar la relación")
            if ask:
                self.bd.delete_filter(("grupos", "relacion", grupo))
                self.load_Treeview_consulta_gru()
                self.load_treeview_consulta_gru_data()
        except IndexError:
            messagebox.showwarning("Alerta", "No has seleccionado ninguna relación")

    ########################################### Widgets #############################################

    def load_gui_grupos_widgets(self):
        """
        Load widgets of Gestor Grupos Gui
        """
        self.titulo = tk.Label(self.gui_grupos, text="Gestor de grupos")
        self.titulo.grid(column=0, row=0, columnspan=3, pady=(10, 15))

        self.load_Treeview_consulta_gru()  # Load Treeview
        self.load_treeview_consulta_gru_data()  # Load data of the Treeview

        self.btn_anadir_gru = tk.Button(self.gui_grupos, text="Nuevo", width="12", height="2",
                                        command=self.anade_gru)
        self.btn_anadir_gru.grid(column=0, row=2, pady=(5, 10), padx=10)

        self.btn_edita_gru = tk.Button(self.gui_grupos, text="Modifica", width="12", height="2",
                                       command=self.edita_gru)
        self.btn_edita_gru.grid(column=1, row=2, pady=(5, 10), padx=10)

        self.btn_salir_gru = tk.Button(self.gui_grupos, text="Elimina", width="12", height="2",
                                       command=self.elimina_gru)
        self.btn_salir_gru.grid(column=2, row=2, pady=(5, 10), padx=10)

    def load_anade_gru_gui(self):
        """Load widgets for anade_gui child guy"""

        self.txt_new_cont_origen = tk.Label(self.anade_gru_grui, text="Contacto Origen")
        self.txt_new_cont_origen.grid(column=0, row=0, columnspan=2, pady=(10, 5))

        self.input_new_cont_origen = tk.Entry(self.anade_gru_grui, width=30)
        self.input_new_cont_origen.grid(column=0, row=1, columnspan=2, padx=20)

        self.txt_new_cont_miembro = tk.Label(self.anade_gru_grui, text="Contacto Miembro")
        self.txt_new_cont_miembro.grid(column=0, row=2, columnspan=2, pady=(20, 5))

        self.input_new_cont_miembro = tk.Entry(self.anade_gru_grui, width=30)
        self.input_new_cont_miembro.grid(column=0, row=3, columnspan=2, padx=20)

        self.txt_new_rel = tk.Label(self.anade_gru_grui, text="Relación")
        self.txt_new_rel.grid(column=0, row=4, columnspan=2, pady=(20, 5))

        self.input_new_rel = tk.Entry(self.anade_gru_grui, width=30)
        self.input_new_rel.grid(column=0, row=5, columnspan=2, padx=20)

        self.btn_register = tk.Button(self.anade_gru_grui, text="Insertar", width="12", height="2",
                                      command=self.anade_gru_grui_insert)
        self.btn_register.grid(column=0, row=6, pady=(15, 10), padx=20)

        self.btn_salir = tk.Button(self.anade_gru_grui, text="Cerrar", width="12", height="2",
                                   command=self.anade_gru_grui_cerrar)
        self.btn_salir.grid(column=1, row=6, pady=(15, 10), padx=20)

    def load_edita_gru_gui(self):
        self.titulo_edita_gru_gui = tk.Label(self.edita_gru_gui, text=("grupo " + self.name_grupo).upper())
        self.titulo_edita_gru_gui.grid(column=0, row=0, columnspan=2, pady=(10, 10))

        self.txt_edit_cont_origen = tk.Label(self.edita_gru_gui, text="Contacto Origen")
        self.txt_edit_cont_origen.grid(column=0, row=1, columnspan=2, pady=(10, 5))

        self.input_edit_cont_origen = tk.Entry(self.edita_gru_gui, width=30)
        self.input_edit_cont_origen.grid(column=0, row=2, columnspan=2, padx=20)

        self.txt_edit_cont_miembro = tk.Label(self.edita_gru_gui, text="Contacto Miembro")
        self.txt_edit_cont_miembro.grid(column=0, row=3, columnspan=2, pady=(20, 5))

        self.input_edit_cont_miembro = tk.Entry(self.edita_gru_gui, width=30)
        self.input_edit_cont_miembro.grid(column=0, row=4, columnspan=2, padx=20)

        self.txt_edit_rel = tk.Label(self.edita_gru_gui, text="Relación")
        self.txt_edit_rel.grid(column=0, row=5, columnspan=2, pady=(20, 5))

        self.input_edit_rel = tk.Entry(self.edita_gru_gui, width=30)
        self.input_edit_rel.grid(column=0, row=6, columnspan=2, padx=20)

        self.btn_edit = tk.Button(self.edita_gru_gui, text="Insertar", width="12", height="2",
                                  command=self.mod_gru)
        self.btn_edit.grid(column=0, row=7, pady=(15, 10), padx=20)

        self.btn_salir = tk.Button(self.edita_gru_gui, text="Cerrar", width="12", height="2",
                                   command=self.close_edita_gru_gui)
        self.btn_salir.grid(column=1, row=7, pady=(15, 10), padx=20)
