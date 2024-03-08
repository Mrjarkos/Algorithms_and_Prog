import tkinter as tk
from tkinter import messagebox
from DBManager import DBManager
from Table import Table
from DB_Info import tables, COMMON_ATTRB

class ListSubjects():
    
    def __init__(self, master, db : DBManager):
        self.db = db
        self.toplevel = tk.Toplevel(master)
        self.toplevel.title("Listar Materias")
        self.toplevel.geometry("800x500")
        self.subject_filter = tk.StringVar()
        self.subject_filter.set("")
        self.facultad = tk.StringVar()
        
        self.build()
        
    def build(self):
        self.frame = tk.Frame(self.toplevel)
        self.facultad_lbl = tk.Label(self.frame, text="Facultad:")
        facultades = set([str(f[0]) for f in self.db.get_materias(properties=["facultad"])])
        self.facultad_entry = tk.OptionMenu(self.frame, self.facultad, *facultades, command=self.load_materias)
        
        self.subject_lbl = tk.Label(self.frame, text="Ver materia")
        self.subject_combobox = tk.OptionMenu(self.frame, self.subject_filter, *[""])
        
        self.facultad_lbl.grid(row=0, column=0, sticky="nw")
        self.facultad_entry.grid(row=0, column=1, sticky="nw")
        
        self.subject_lbl.grid(column=0, row=1, sticky="nw")
        self.subject_combobox.grid(column=1, row=1, sticky="nw")

        self.frame.grid(padx=10, pady=10, sticky="nswe")
        
        self.header = self.db.sort_properties(COMMON_ATTRB, exclude=["id"])
        self.table = Table(self.frame, header=self.header+["Rol"], double_click_command=None)
        
        self.table.grid(column=0, row=2, columnspan=5, rowspan=4)
        
    def load_users(self, materia):
        self.subject_filter.set(materia)
        if materia == "":
            regs = {}
        else: 
            materia_id = [f[0] for f in self.db.get_materias(properties=["id"], filter={"nombre": materia})][0]
            regs = self.db.get_proff_students_from_subject( materia_id, self.header)
        self.usrs = []
        for key, item in regs.items():
            self.usrs += [tuple(list(usr)+[key]) for usr in item]
        self.usrs.sort()
        self.table.set_data(self.usrs)
        self.table.update()
        
    def show(self):
        self.toplevel.grab_set()  # Block events in other windows
        self.toplevel.wait_window()  # Wait until the dialog is closed
    
    def load_materias(self, event):
        facultad = self.facultad.get()
        materias =  list([str(f[0]) for f in self.db.get_materias(properties=["nombre"], filter={"facultad": facultad})])
        self.subject_combobox["menu"].delete(0, "end")

        for materia in materias:
            self.subject_combobox["menu"].add_command(label=materia, command=lambda m=materia: self.load_users(m))
           