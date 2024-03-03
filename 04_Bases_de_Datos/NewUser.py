import tkinter as tk
from tkinter import messagebox
from DBManager import DBManager

ROLES = {
    "estudiante" : lambda frame: FrameStudent(frame),
    "profesor" : lambda frame: FrameProfessor(frame)
}

class FrameProfessor(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        self.especialidad = tk.StringVar()
        self.subject_filter = tk.StringVar()
        self.subject_list = tk.Variable(value=())
        self._subjects = []
        super().__init__(master, *args, **kwargs)
        self.frame = tk.Frame(master)
        self.build()
    
    def build(self):
        self.especialidad_lbl = tk.Label(self.frame, text="Especialidad:")
        self.especialidad_entry = tk.Entry(self.frame, textvariable=self.especialidad)
        
        self.subject_lbl = tk.Label(self.frame, text="Añadir materia:")
        #self.subject_combobox = tk.OptionMenu(self.frame, self.subject_filter)#, *SUBJECTS, command=self.add_subject)
        self.subject_lbl_list = tk.Listbox(self.frame)
        
        self.especialidad_lbl.grid(column=0, row=0, sticky="nw")
        self.especialidad_entry.grid(column=1, row=0, sticky="nw")
        self.subject_lbl.grid(column=0, row=1, sticky="nw")
        #self.subject_combobox.grid(column=1, row=1, sticky="nw")
        self.subject_lbl_list.grid(column=0, columnspan=1, row=2, sticky="nw")
        self.frame.grid()
        
    def add_subject(self, selection):
        current_selection = self.subject_filter.get()
        if current_selection not in self._subjects:
            self.subject_lbl_list.insert(0, current_selection)
            self._subjects.append(current_selection)

class FrameStudent(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame = tk.Frame(self)
        self.subject_filter = tk.StringVar()
        self.semester = tk.IntVar()
        self.carrera = tk.StringVar()
        self.subject_list_str = tk.StringVar()
        self._subjects = []
        self.build()
        
    def build(self):
        
        self.semester_lbl = tk.Label(self.frame, text="Semestre:")
        self.semester_entry = tk.Entry(self.frame, textvariable=self.semester)
        self.carrera_lbl = tk.Label(self.frame, text="Carrera:")
        self.carrera_entry = tk.Entry(self.frame, textvariable=self.carrera)
        self.subject_lbl = tk.Label(self.frame, text="Añadir materias:")
        #self.subject_combobox = tk.OptionMenu(self.frame, self.subject_filter, *SUBJECTS, command=self.add_subject)
        self.subject_lbl_list = tk.Listbox(self.frame)
        
        self.semester_lbl.grid(column=0, row=0, sticky="nw")
        self.semester_entry.grid(column=1, row=0, sticky="nw")
        self.carrera_lbl.grid(column=0, row=1, sticky="nw")
        self.carrera_entry.grid(column=1, row=1, sticky="nw")
        self.subject_lbl.grid(column=0, row=2, sticky="nw")
        #self.subject_combobox.grid(column=1, row=2, sticky="nw")
        self.subject_lbl_list.grid(column=0, columnspan=1, row=2, sticky="nw")
        self.frame.grid()
        
    def add_subject(self, selection):
        current_selection = self.subject_filter.get()
        if current_selection not in self._subjects:
            self.subject_lbl_list.insert(0, current_selection)
            self._subjects.append(current_selection)

class NewUser():
    
    def __init__(self, master, db : DBManager, user : tuple | None = None):
        self.db = db
        self.toplevel = tk.Toplevel(master)
        self.toplevel.title("Crear Usuario")
        self.toplevel.geometry("800x500")
        self.first_name = tk.StringVar()
        self.id = tk.StringVar()
        self.edad = tk.IntVar()
        self.facultad = tk.StringVar()
        self.rol_filter = tk.StringVar()
        self.rol_filter.set("estudiante")
        self.result = False 
        self.new = True
        self.build()
        if user:
            self.user = user
            self.new = False
            self.load_data(user)
        
    def build(self):
        self.frame = tk.Frame(self.toplevel)
        
        self.first_name_lbl = tk.Label(self.frame, text="Nombre:")
        self.first_name_entry = tk.Entry(self.frame, textvariable=self.first_name)
        self.id_lbl = tk.Label(self.frame, text="Identificacion:")
        self.id_entry = tk.Entry(self.frame, textvariable=self.id)

        self.edad_lbl = tk.Label(self.frame, text="Edad:")
        self.edad_entry = tk.Entry(self.frame, textvariable=self.edad)
        self.facultad_lbl = tk.Label(self.frame, text="Facultad:")
        self.facultad_entry = tk.Entry(self.frame, textvariable=self.facultad)
        self.rol_lbl = tk.Label(self.frame, text="Tipo de Usuario")
        self.rol_combobox = tk.OptionMenu(self.frame, self.rol_filter, *list(ROLES.keys()), command=self.display_rol_frame)
        self.rol_frame = tk.Frame(self.frame)
        self.create_btn = tk.Button(self.frame, text="Crear Usuario", command=self.validate_data)
        
        self.first_name_lbl.grid(row=0, column=0, sticky="nw")
        self.first_name_entry.grid(row=0, column=1, sticky="nw")
        self.id_lbl.grid(row=1, column=0, sticky="nw")
        self.id_entry.grid(row=1, column=1, sticky="nw")
        self.edad_lbl.grid(row=2, column=0, sticky="nw")
        self.edad_entry.grid(row=2, column=1, sticky="nw")
        self.facultad_lbl.grid(row=3, column=0, sticky="nw")
        self.facultad_entry.grid(row=3, column=1, sticky="nw")
        
        self.rol_lbl.grid(row=5, column=0, sticky="nw")
        self.rol_combobox.grid(row=5, column=1, sticky="nw")

        self.create_btn.grid(row=10, column=3, sticky="nw")
        self.frame.grid(padx=10, pady=10, sticky="nswe")
        
        self.display_rol_frame(None)
    
    def display_rol_frame(self, selection):
        self.rol_frame.destroy()
        self.rol_frame = tk.Frame(self.frame)
        self.rol_frame.children.clear()
        if self.rol_filter.get() is not None:
            self.rol_frame_child = ROLES[self.rol_filter.get()](self.rol_frame)
            self.rol_frame_child.grid()
            self.rol_frame.grid(row=6, column=0, columnspan=3, rowspan=4, sticky="nswe")
    
    def validate_data(self):
        if any([
            not element.get() for element in [self.first_name, self.id,
                                        self.edad, self.facultad]
        ]):
            messagebox.showerror("Elementos faltantes", "Por favor diligencie todos los campos")
            return
        unique=self.db.validate_unique_ident(self.id.get())
        if self.new:
            if not unique:
                messagebox.showerror("Id existe", "Su numero de documento ya se encuentra registrado")
                return
            
            self.add_usr()
        else:
            if unique:
                messagebox.showerror("Id no existe", "No se encontro id a modificar")
                return
            
            self.modify_usr()
        self.result = True
        self.toplevel.destroy()
    
    def show(self):
        self.toplevel.grab_set()  # Block events in other windows
        self.toplevel.wait_window()  # Wait until the dialog is closed
        return self.result
    
    def load_data(self, user):
        
        
        rol = user[-1]
        
        self.first_name.set(user[1])
        self.id.set(user[0])
        self.edad.set(int(user[2]))
        self.rol_filter.set(rol)
        self.display_rol_frame(None)
        if rol == "estudiante":
            usr = self.db.get_estudiantes(properties = ["facultad", "carrera", "semestre"],
                                          filter={"identificacion": user[0]})[0]
            print(f"estudiante={usr}")
            self.rol_frame_child.semester.set(usr[2])
            self.rol_frame_child.carrera.set(usr[1])
            self.facultad.set(usr[0])
        elif rol == "profesor":
            usr = self.db.get_profesores(properties = ["facultad", "especialidad"],
                                         filter={"identificacion": user[0]})[0]
            print(f"profesor={usr}")
            self.facultad.set(usr[0])
            self.rol_frame_child.especialidad.set(usr[1])
            
    
    def modify_usr(self):
        nombre = self.first_name.get()
        id = self.id.get()
        edad = self.edad.get()
        facultad = self.facultad.get()

        selection = self.rol_filter.get()
        if selection == "estudiante":
            ## Create Student
            subjects = self.rol_frame_child._subjects
            semestre = self.rol_frame_child.semester.get()
            carrera = self.rol_frame_child.carrera.get()
            self.db.update_estudiante(nombre, id, edad, semestre, carrera, facultad)
        elif selection == "profesor":
            especialidad = self.rol_frame_child.especialidad.get()
            subjects = self.rol_frame_child._subjects
            self.db.update_profesor(nombre, id, edad, facultad, especialidad) 
    
    def add_usr(self):
        # Id, nombre, identificacion, edad  ... facultad
        nombre = self.first_name.get()
        id = self.id.get()
        edad = self.edad.get()
        facultad = self.facultad.get()

        selection = self.rol_filter.get()
        if selection == "estudiante":
            ## Create Student
            subjects = self.rol_frame_child._subjects
            semestre = self.rol_frame_child.semester.get()
            carrera = self.rol_frame_child.carrera.get()
            self.db.insert_estudiante(nombre, id, edad, semestre, carrera, facultad)   
        elif selection == "profesor":
            especialidad = self.rol_frame_child.especialidad.get()
            subjects = self.rol_frame_child._subjects
            self.db.insert_profesor(nombre, id, edad, facultad, especialidad) 
        # else:
        #     job = self.rol_frame_child.job.get()
        #     department = self.rol_frame_child.department.get()
        #     base_salary = self.rol_frame_child.base_salary.get()
        #     person = Administrativo(tomasino=person, 
        #                       job=job, department=department, base_salary=base_salary)
            
    # "Administrativo": lambda frame: FrameAdmin(frame),
    # "Profesor": lambda frame: FrameProfessor(frame)
        messagebox.showinfo("Operacion exitosa", f"{selection} creado")
        return 
    
        
        
        
        