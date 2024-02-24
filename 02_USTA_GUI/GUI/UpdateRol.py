import tkinter as tk 
from tkinter import messagebox

from GUI.utils import USER_TYPE_LIST

from GUI.NewUser import ROLES
from Objects.Estudiante import Estudiante
from Objects.Administrativo import Administrativo
from Objects.Profesor import Profesor

class UpdateRol():
    
    def __init__(self, master):
        self.toplevel = tk.Toplevel(master)
        self.toplevel.title("Actualizar Rol")
        self.toplevel.geometry("500x500")
        self.cod = tk.IntVar()
        self.password = tk.StringVar()
        self.rol_filter = tk.StringVar()
        self.rol_filter.set(USER_TYPE_LIST[0])
        self.build()
        
    def build(self):
        self.frame = tk.Frame(self.toplevel)
        self.cod_lbl = tk.Label(self.frame, text="Codigo:")
        self.cod_entry = tk.Entry(self.frame, textvariable=self.cod)
        self.rol_lbl = tk.Label(self.frame, text="Tipo de Usuario")
        self.rol_combobox = tk.OptionMenu(self.frame, self.rol_filter, *USER_TYPE_LIST, command=self.display_rol_frame)
        self.rol_frame = tk.Frame(self.frame)
        self.create_btn = tk.Button(self.frame, text="Añadir rol a Usuario", command=self.toplevel.destroy)
        
        self.cod_lbl.grid(row=0, column=0, sticky="nw")
        self.cod_entry.grid(row=0, column=1, sticky="nw")
        self.rol_lbl.grid(row=1, column=0, sticky="nw")
        self.rol_combobox.grid(row=1, column=1, sticky="nw")
        
        self.create_btn.grid(row=5, column=3, sticky="nw")
        self.frame.grid(padx=10, pady=10, sticky="nswe")
        
        self.display_rol_frame(None)
    
    def display_rol_frame(self, selection):
        self.rol_frame.destroy()
        self.rol_frame = tk.Frame(self.frame)
        self.rol_frame.children.clear()
        if self.rol_filter.get() is not None:
            self.rol_frame_child = ROLES[self.rol_filter.get()](self.rol_frame)
            self.rol_frame_child.grid()
            self.rol_frame.grid(row=2, column=0, columnspan=3, rowspan=4, sticky="nswe")
            
    def show(self):
        self.toplevel.grab_set()  # Block events in other windows
        self.toplevel.wait_window()  # Wait until the dialog is closed
        return self.update_usr()
    
    def update_usr(self):
        params = []
        selection = self.rol_filter.get()
        if selection == "Estudiante":
                ## Create Student
            obj_typ = Estudiante
            subjects = self.rol_frame_child._subjects
            semestre = self.rol_frame_child.semester.get()
            params = (subjects, semestre)
        elif selection == "Profesor":
            obj_typ = Profesor
            job = self.rol_frame_child.job.get()
            department = self.rol_frame_child.department.get()
            base_salary = self.rol_frame_child.base_salary.get()
            subjects = self.rol_frame_child._subjects
            params = (job, department, base_salary, subjects)
        else:
            obj_typ = Administrativo
            job = self.rol_frame_child.job.get()
            department = self.rol_frame_child.department.get()
            base_salary = self.rol_frame_child.base_salary.get()
            params = (job, department, base_salary)

        return (
            obj_typ, #Type
            self.cod.get(), 
            params
        )