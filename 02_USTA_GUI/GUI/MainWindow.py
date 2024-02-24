import tkinter as tk
from tkinter import messagebox

from Objects.Tomasino import Tomasino
from Objects.Profesor import Profesor
from Objects.Estudiante import Estudiante
from Objects.Administrativo import Administrativo
from GUI.Table import Table
from GUI.NewUser import NewUser
from GUI.UpdatePassword import UpdatePassword
from GUI.UpdateRol import UpdateRol

from GUI.utils import USER_TYPE_LIST, USER_TYPE_DICT

class MainWindow(tk.Frame):
    
    Users: list[Tomasino] = []
    
    def __init__(self, parent, *args, **kwargs):
        self.attr_filter = tk.StringVar()
        self.rol_filter = tk.StringVar()
        self.search = tk.StringVar()
        
        self.att_list = Tomasino.get_public_format_properties()
        self.attr_filter.set("")
        self.rol_filter.set("")
        
        self.view_users = self.Users
        
        super().__init__(parent, *args, kwargs)
        self.build()
        self.grid(sticky="nswe", padx=10, pady=10)
    
    def build(self):
        ### Basic Functions
        self.add_tomasino_btn = tk.Button(self, text="Añadir Tomasino", command=self.add_usr)
        self.update_pssw_btn = tk.Button(self, text="Cambiar clave", command=self.update_pssw)
        self.update_rol_btn = tk.Button(self, text="Añadir rol", command=self.update_rol)
        
        ### Search
        self.search_lbl = tk.Label(self, text="Buscar Usuario")
        self.search_entry = tk.Entry(self, textvariable=self.search)
        self.property_lbl= tk.Label(self, text="Buscar por Atributo")
        self.property_combobox = tk.OptionMenu(self, self.attr_filter, *self.att_list+[""], command=self.filter_by_attr)
        self.rol_lbl= tk.Label(self, text="Filtrar por Rol")
        self.rol_combobox = tk.OptionMenu(self, self.rol_filter, *USER_TYPE_LIST+[""], command=self.filter_by_rol)
        
        ### Table
        self.table = Table(self, header=self.att_list)
        
        self.add_tomasino_btn.grid  (column=0, row=0, sticky="nw", pady=10, columnspan=1)
        self.update_pssw_btn.grid   (column=2, row=0, sticky="nw", pady=10, columnspan=1)
        self.update_rol_btn.grid    (column=4, row=0, sticky="nw", pady=10, columnspan=1)
        self.search_lbl.grid        (column=0, row=1, sticky="nw", pady=10)
        self.search_entry.grid      (column=1, row=1, sticky="nw", pady=10)
        self.property_lbl.grid      (column=2, row=1, sticky="nw", pady=10)
        self.property_combobox.grid (column=3, row=1, sticky="nw", pady=10)
        self.rol_lbl.grid           (column=4, row=1, sticky="nw", pady=10)
        self.rol_combobox.grid      (column=5, row=1, sticky="nw", pady=10)
        self.table.grid(column=0, row=2, columnspan=5, rowspan=4)
        
        self.search_entry.bind('<KeyRelease>', self.filter_by_attr)
    
    def update_Table(self, usr_list : list):
        users = [user.as_list() for user in usr_list]
        self.table.set_data(users)
        self.table.update()
    
    def filter_by_attr(self, sel):
        sel = self.attr_filter.get()
        txt = self.search.get()
        self.filter_by_rol(None)
        if txt == "":
            ### Display All
            users = self.view_users
        elif sel == "":
            ## Search all
            users = [user for user in self.view_users if txt in ",".join(user.as_str_list())]
        else:
            ## Search only attrib
            users = [user for user in self.view_users if txt in str(user.get_attribute_from_format(sel))]
            
        self.update_Table(users)
        
    
    def filter_by_rol(self, sel):
        sel = self.rol_filter.get()
        if sel == "":
            ### Display All
            self.view_users = self.Users
        else:
            self.view_users = [user for user in self.Users if isinstance(user, USER_TYPE_DICT[sel])]
        self.update_Table(self.view_users)

    def update_rol(self):
        
        usr_typ, cod, params = UpdateRol(self).show()
        
        if not self.check_cod(cod):
            messagebox.showerror("Codigo Error", f"No existe usuario con codigo {cod}")
            return
        
        ## Load User
        user = self.get_usr(cod)
        
        if isinstance(user, usr_typ):
            messagebox.showerror("Tipo Error", f"El usuario con codigo {cod} ya es un {usr_typ.__name__}")
            return 
        
        new_rol = usr_typ(tomasino=user, *params)
        
        self.Users.append(new_rol)
        self.view_users = self.Users
        self.table.update()
    
    def get_usr(self, cod):
        if not self.check_cod(cod):
            return None
        codes = [user.cod for user in self.Users]
        idx = codes.index(cod)
        return self.Users[idx]

    def add_usr(self):
        cod = len(self.Users)
        user = NewUser(self, cod).show()
        if user is not None:
            self.Users.append(user)
            self.view_users = self.Users
            self.table.insert(user.as_list())
            self.table.update()
    
    def check_cod(self, cod):
        codes =  [user.cod for user in self.Users]
        return cod in codes, codes
    
    def update_pssw(self):       
        result = UpdatePassword(self).show()
        if result is None:
            return
        cod, old_pssw, new_pssw = result
        
        result, codes = self.check_cod(cod)
        if not result:
            messagebox.showerror("Codigo Error", f"No existe usuario con codigo {cod}")
            return 
        
        idx = codes.index(cod)
        result = self.Users[idx].update_password(old_pssw, new_pssw)
        if result is None:
            messagebox.showinfo("Operacion exitosa", "Contraseña actualizada correctamente")
        else:
            messagebox.showerror("Error Contraseña", result)
            