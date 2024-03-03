import tkinter as tk
from tkinter import messagebox

from DBManager import DBManager
from Table import Table
from NewUser import NewUser
from DB_Info import tables, COMMON_ATTRB

class MainWindow(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        self.Db = DBManager()
        self.usrs = []
        self.attr_filter = tk.StringVar()
        self.rol_filter = tk.StringVar()
        self.search = tk.StringVar()
        
        self.attr_filter.set("")
        self.rol_filter.set("")
        
        super().__init__(parent, *args, **kwargs)
        self.build()
        self.grid(sticky="nswe", padx=10, pady=10)
        
    def build(self):
        ### Basic Functions
        self.add_tomasino_btn = tk.Button(self, text="Añadir Tomasino", command=self.new_user)
        
        ### Search
        self.search_lbl = tk.Label(self, text="Buscar Usuario ID")
        self.search_entry = tk.Entry(self, textvariable=self.search)
        self.rol_lbl= tk.Label(self, text="Filtrar por Rol")
        self.rol_combobox = tk.OptionMenu(self, self.rol_filter, *list(tables.keys())+[""])#, command=self.filter_by_rol)
        
        ### Table
        self.header = self.Db.sort_properties(COMMON_ATTRB, exclude=["id"])
        self.table = Table(self, header=self.header+["Rol"], double_click_command=self.edit_user)
        
        self.add_tomasino_btn.grid  (column=0, row=0, sticky="nw", pady=10, columnspan=1)
        self.search_lbl.grid        (column=0, row=1, sticky="nw", pady=10)
        self.search_entry.grid      (column=1, row=1, sticky="nw", pady=10)
        #self.property_combobox.grid (column=3, row=1, sticky="nw", pady=10)
        self.rol_lbl.grid           (column=4, row=1, sticky="nw", pady=10)
        self.rol_combobox.grid      (column=5, row=1, sticky="nw", pady=10)
        self.table.grid(column=0, row=2, columnspan=5, rowspan=4)
        
        self.load_users()
        self.search_entry.bind('<KeyRelease>', self.filter_by_id)
    
    def filter_by_id(self, event):
        # req: Permita que se pueda buscar un usuario a traves de su ID y mostrarlo.
        id = self.search.get()
        if id:
            self.table.set_data([usr for usr in self.usrs if id in usr[0]])
            self.table.update()
        else: 
            self.load_users()
    
    def load_users(self):
        regs = self.Db.get_proff_students(self.header)
        self.usrs = []
        for key, item in regs.items():
            self.usrs += [tuple(list(usr)+[key]) for usr in item]
        self.usrs.sort()
        self.table.set_data(self.usrs)
        self.table.update()

    def new_user(self):
        # req: Permita que se puedan ingresar nuevos registros y se almacenen en BD.
        NewUser(self, self.Db).show()
        self.load_users()
        
    def edit_user(self, row : int):
        usr = tuple(self.table.data[row])
        # req: Permita modificar registros de cualquier tabla.
        NewUser(self, self.Db, usr).show()
        self.load_users()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Administrar Tomasinos")
    root.geometry("800x500")
    main = MainWindow(root)
    root.mainloop()
    