import tkinter as tk
from tkinter import messagebox
from DBManager import DBManager

ROLES = {
    "estudiante" : lambda frame: FrameStudent(frame),
    "docente" : lambda frame: FrameProfessor(frame)
}

class FrameProfessor(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        self.especialidad = tk.StringVar()
        super().__init__(master, *args, **kwargs)
        self.frame = tk.Frame(master)
        self.build()
    
    def build(self):
        self.especialidad_lbl = tk.Label(self.frame, text="Especialidad:")
        self.especialidad_entry = tk.Entry(self.frame, textvariable=self.especialidad)
        self.especialidad_lbl.grid(column=0, row=0, sticky="nw")
        self.especialidad_entry.grid(column=1, row=0, sticky="nw")
        self.frame.grid()

class FrameStudent(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame = tk.Frame(self)
        self.semester = tk.IntVar()
        self.carrera = tk.StringVar()
        self.build()
        
    def build(self):
        
        self.semester_lbl = tk.Label(self.frame, text="Semestre:")
        self.semester_entry = tk.Entry(self.frame, textvariable=self.semester)
        self.carrera_lbl = tk.Label(self.frame, text="Carrera:")
        self.carrera_entry = tk.Entry(self.frame, textvariable=self.carrera)
        
        self.semester_lbl.grid(column=0, row=0, sticky="nw")
        self.semester_entry.grid(column=1, row=0, sticky="nw")
        self.carrera_lbl.grid(column=0, row=1, sticky="nw")
        self.carrera_entry.grid(column=1, row=1, sticky="nw")
        self.frame.grid()

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
        self.subject_filter = tk.StringVar()
        self.subject_filter.set("")
        self._subjects = []
        self.subject_list = tk.Variable(value=())
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
        facultades = set([str(f[0]) for f in self.db.get_materias(properties=["facultad"])])
        self.facultad_entry = tk.OptionMenu(self.frame, self.facultad, *facultades, command=self.load_materias)
        self.rol_lbl = tk.Label(self.frame, text="Tipo de Usuario")
        self.rol_combobox = tk.OptionMenu(self.frame, self.rol_filter, *list(ROLES.keys()), command=self.display_rol_frame)
        self.rol_frame = tk.Frame(self.frame)
        
        self.subject_lbl = tk.Label(self.frame, text="Añadir materia:")
        self.subject_combobox = tk.OptionMenu(self.frame, self.subject_filter, *[""])
        self.subject_lbl_list = tk.Listbox(self.frame, width=40)
         
        self.create_btn = tk.Button(self.frame, text="Crear Usuario", command=self.validate_data)  
        
        self.first_name_lbl.grid(row=0, column=0, sticky="nw")
        self.first_name_entry.grid(row=0, column=1, sticky="nw")
        self.id_lbl.grid(row=1, column=0, sticky="nw")
        self.id_entry.grid(row=1, column=1, sticky="nw")
        self.edad_lbl.grid(row=2, column=0, sticky="nw")
        self.edad_entry.grid(row=2, column=1, sticky="nw")
        self.facultad_lbl.grid(row=3, column=0, sticky="nw")
        self.facultad_entry.grid(row=3, column=1, sticky="nw")
        
        self.subject_lbl.grid(column=0, row=8, sticky="nw")
        self.subject_combobox.grid(column=1, row=8, sticky="nw")
        self.subject_lbl_list.grid(column=0, columnspan=2, row=9, sticky="nw")
        
        self.rol_lbl.grid(row=5, column=0, sticky="nw")
        self.rol_combobox.grid(row=5, column=1, sticky="nw")

        self.create_btn.grid(row=11, column=3, sticky="nw")
        self.frame.grid(padx=10, pady=10, sticky="nswe")
        
        self.display_rol_frame(None)
        self.subject_lbl_list.bind("<Double-1>", self.remove_selected_item)
    
    def display_rol_frame(self, selection):
        self.rol_frame.destroy()
        self.rol_frame = tk.Frame(self.frame)
        self.rol_frame.children.clear()
        if self.rol_filter.get() is not None:
            self.rol_frame_child = ROLES[self.rol_filter.get()](self.rol_frame)
            self.rol_frame_child.grid()
            self.rol_frame.grid(row=6, column=0, columnspan=3, rowspan=2, sticky="nswe")
    
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
            
            res = self.add_usr()
        else:
            if unique:
                messagebox.showerror("Id no existe", "No se encontro id a modificar")
                return
            
            res = self.modify_usr()
            
        if not res:
            return
        self.result = True
        self.toplevel.destroy()
    
    def show(self):
        self.toplevel.grab_set()  # Block events in other windows
        self.toplevel.wait_window()  # Wait until the dialog is closed
        return self.result
    
    def load_materias(self, event):
        # When changing Faculty, you have to start again from the beginning 
        self._subjects = []
        self.subject_lbl_list.delete(0, tk.END)
        
        facultad = self.facultad.get()
        materias =  list([str(f[0]) for f in self.db.get_materias(properties=["nombre"], filter={"facultad": facultad})])
        self.subject_combobox["menu"].delete(0, "end")

        for materia in materias:
            self.subject_combobox["menu"].add_command(label=materia, command=lambda m=materia: self.add_subject(m))
           
    def add_subject(self, subject):
        self.subject_filter.set(subject)
        if subject not in self._subjects:
            self.subject_lbl_list.insert(0, subject)
            self._subjects.append(subject)
  
    def remove_selected_item(self, event):
        selected_index = self.subject_lbl_list.curselection()
        if selected_index:
            self.subject_lbl_list.delete(selected_index)
            self._subjects.pop(selected_index[0])
    
    def load_data(self, user):       
        rol = user[-1]
        estudiante_id = None
        docente_id = None
        self.first_name.set(user[1])
        self.id.set(user[0])
        self.edad.set(int(user[2]))
        self.rol_filter.set(rol)
        self.display_rol_frame(None)
        if rol == "estudiante":
            usr = self.db.get_estudiantes(properties = ["id", "facultad", "carrera", "semestre"],
                                          filter={"identificacion": user[0]})[0]
            self.rol_frame_child.semester.set(usr[3])
            self.rol_frame_child.carrera.set(usr[2])
            self.facultad.set(usr[1])
            self.subject_lbl_list
            estudiante_id = usr[0]
        elif rol == "docente":
            usr = self.db.get_profesores(properties = ["id", "facultad", "especialidad"],
                                         filter={"identificacion": user[0]})[0]
            self.facultad.set(usr[1])
            self.rol_frame_child.especialidad.set(usr[2])
            docente_id = usr[0]
        
        self.create_btn["text"] = "Actualizar usuario"
        self.id_entry.config(state = "disabled")
        self.facultad_entry.config(state = "disabled")
        self.load_materias(None)
        
        # Get Materias
        #
        materias = self.db.get_materia_props_from_estudiante_profesor(["nombre"], estudiante_id, docente_id)
        
        for m in materias:
            self.subject_lbl_list.insert(0, m[0])
            self._subjects.append(m[0])
        
            
    def modify_usr(self):
        estudiante_id = None
        docente_id = None
        nombre = self.first_name.get()
        id = self.id.get()
        edad = self.edad.get()
        facultad = self.facultad.get()

        selection = self.rol_filter.get()
        if selection == "estudiante":
            ## Create Student
            semestre = self.rol_frame_child.semester.get()
            carrera = self.rol_frame_child.carrera.get()
            estudiante_id = self.db.update_estudiante(nombre, id, edad, semestre, carrera, facultad)
        elif selection == "docente":
            especialidad = self.rol_frame_child.especialidad.get()
            docente_id = self.db.update_profesor(nombre, id, edad, facultad, especialidad) 
        
        materias = self.db.get_materia_props_from_estudiante_profesor(properties=["id", "nombre"],
                                                                    estudiante_id=estudiante_id,
                                                                    profesor_id=docente_id)
        
        # Delete subjects
        delete_subjects_id = [id for id, name in materias if name not in self._subjects]
        for s in delete_subjects_id:
            self.db.delete_materias_estudiantes_profesor(s, estudiante_id, docente_id)
            
        names = [name for id, name in materias]
        add_subjects = [s for s in self._subjects if s not in names]
        for m in add_subjects:    
            # Get materia_id
            # req: Una materia solo puede tener un solo profesor
            # TODO:
            materia_id = [f[0] for f in self.db.get_materias(properties=["id"], filter={"nombre": m})][0]
            if selection == "docente":
                # Validate there is no another professor already assigned
                matches = self.db.get_materias_estudiantes_profesor(properties=["docente_id"], filter={"materia_id": materia_id})
                if matches:
                    messagebox.showerror("Materia asignada", f"Lo sentimos, la materia {m} ya está asignada")
                    return False
            
            self.db.insert_materias_estudiantes_profesor(materia_id, estudiante_id, docente_id)
        return True
    
    def add_usr(self):
        
        estudiante_id = None
        docente_id = None
        # Id, nombre, identificacion, edad  ... facultad
        nombre = self.first_name.get()
        id = self.id.get()
        edad = self.edad.get()
        facultad = self.facultad.get()
        selection = self.rol_filter.get()
        if selection == "estudiante":
            ## Create Student
            semestre = self.rol_frame_child.semester.get()
            carrera = self.rol_frame_child.carrera.get()
            estudiante_id = self.db.insert_estudiante(nombre, id, edad, semestre, carrera, facultad)
        elif selection == "docente":
            especialidad = self.rol_frame_child.especialidad.get()
            docente_id = self.db.insert_profesor(nombre, id, edad, facultad, especialidad) 
        
        for m in self._subjects:    
            # Get materia_id
            materia_id = [f[0] for f in self.db.get_materias(properties=["id"], filter={"nombre": m})][0]
            
            if selection == "docente":
                # Validate there is no another professor already assigned
                matches = self.db.get_materias_estudiantes_profesor(properties=["docente_id"], filter={"materia_id": materia_id})
                if matches:
                    messagebox.showerror("Materia asignada", f"Lo sentimos, la materia {m} ya está asignada")
                    return False    
            # req: Una materia solo puede tener un solo profesor
            # TODO:
            self.db.insert_materias_estudiantes_profesor(materia_id, estudiante_id, docente_id)
            
        messagebox.showinfo("Operacion exitosa", f"{selection} creado")
        return True
    
        
        
        
        