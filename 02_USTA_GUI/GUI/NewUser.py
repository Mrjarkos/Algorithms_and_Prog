import tkinter as tk
from tkinter import messagebox
from GUI.utils import USER_TYPE_LIST
from Objects.Tomasino import Tomasino
from Objects.Estudiante import Estudiante
from Objects.Administrativo import Administrativo
from Objects.Profesor import Profesor

USTA_DOMAIN = "@usantotomas.edu.co"

SUBJECTS = [
    "Física Mecánica y Termodinámica",
    "Álgebra Lineal",
    "Cálculo Diferencial",
    "Fundamentos de Circuitos",
    "Introducción a la Ingeniería",
    "Filosofía Institucional",
    "Cátedra Henri Didón",
]

ROLES = {
    Estudiante.__name__ : lambda frame: FrameStudent(frame),
    Administrativo.__name__ : lambda frame: FrameEmployee(frame),
    Profesor.__name__ : lambda frame: FrameProfessor(frame)
}

class FrameEmployee(tk.Frame):
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame = tk.Frame(master)
        self.job = tk.StringVar()
        self.department = tk.StringVar()
        self.base_salary = tk.DoubleVar()
        self.build()
        
    def build(self):
        self.job_lbl = tk.Label(self.frame, text="Cargo:")
        self.job_entry = tk.Entry(self.frame, textvariable=self.job)
        self.department_lbl = tk.Label(self.frame, text="Departamento:")
        self.department_entry = tk.Entry(self.frame, textvariable=self.department)
        self.base_salary_lbl = tk.Label(self.frame, text="Salario Base")
        self.base_salary_entry = tk.Entry(self.frame, textvariable=self.base_salary)
        
        self.job_lbl.grid(column=0, row=0, sticky="nw")
        self.job_entry.grid(column=1, row=0, sticky="nw")
        self.department_lbl.grid(column=0, row=1, sticky="nw")
        self.department_entry.grid(column=1, row=1, sticky="nw")
        self.base_salary_lbl.grid(column=0, row=2, sticky="nw")
        self.base_salary_entry.grid(column=1, row=2, sticky="nw")
        self.frame.grid()

class FrameAdmin(FrameEmployee):
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

class FrameProfessor(FrameEmployee):

    def __init__(self, master, *args, **kwargs):
        self.subject_filter = tk.StringVar()
        self.subject_list = tk.Variable(value=())
        self._subjects = []
        super().__init__(master, *args, **kwargs)
        #self.frame = tk.Frame(master)
        #self.build()
    
    def build(self):
        super().build()
        self.subject_lbl = tk.Label(self.frame, text="Añadir materia:")
        self.subject_combobox = tk.OptionMenu(self.frame, self.subject_filter, *SUBJECTS, command=self.add_subject)
        self.subject_lbl_list = tk.Listbox(self.frame)
        
        self.subject_lbl.grid(column=0, row=3, sticky="nw")
        self.subject_combobox.grid(column=1, row=3, sticky="nw")
        self.subject_lbl_list.grid(column=0, columnspan=1, row=4, sticky="nw")
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
        self.subject_list_str = tk.StringVar()
        self._subjects = []
        self.build()
        
    def build(self):
        
        self.semester_lbl = tk.Label(self.frame, text="Semestre:")
        self.semester_entry = tk.Entry(self.frame, textvariable=self.semester)
        self.subject_lbl = tk.Label(self.frame, text="Añadir materia:")
        self.subject_combobox = tk.OptionMenu(self.frame, self.subject_filter, *SUBJECTS, command=self.add_subject)
        self.subject_lbl_list = tk.Listbox(self.frame)
        
        self.semester_lbl.grid(column=0, row=0, sticky="nw")
        self.semester_entry.grid(column=1, row=0, sticky="nw")
        self.subject_lbl.grid(column=0, row=1, sticky="nw")
        self.subject_combobox.grid(column=1, row=1, sticky="nw")
        self.subject_lbl_list.grid(column=0, columnspan=1, row=2, sticky="nw")
        self.frame.grid()
        
    def add_subject(self, selection):
        current_selection = self.subject_filter.get()
        if current_selection not in self._subjects:
            self.subject_lbl_list.insert(0, current_selection)
            self._subjects.append(current_selection)

class NewUser():
    
    def __init__(self, master, cod):
        self.cod = cod
        self.toplevel = tk.Toplevel(master)
        self.toplevel.title("Crear Usuario")
        self.toplevel.geometry("800x500")
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.id = tk.IntVar()
        self.password = tk.StringVar()
        self.password_verification = tk.StringVar()
        self.rol_filter = tk.StringVar()
        self.rol_filter.set(USER_TYPE_LIST[0])
        self.build()
        
    def build(self):
        self.frame = tk.Frame(self.toplevel)
        
        self.first_name_lbl = tk.Label(self.frame, text="Nombres:")
        self.first_name_entry = tk.Entry(self.frame, textvariable=self.first_name)
        self.last_name_lbl = tk.Label(self.frame, text="Apellidos:")
        self.last_name_entry = tk.Entry(self.frame, textvariable=self.last_name)
        self.id_lbl = tk.Label(self.frame, text="Identificacion:")
        self.id_entry = tk.Entry(self.frame, textvariable=self.id)
        ## Codigo es generado automaticamente
        ## Email es generado automaticamente
        self.password_lbl = tk.Label(self.frame, text="Contraseña: ")
        self.password_entry = tk.Entry(self.frame, textvariable=self.password)        
        self.password_2_lbl = tk.Label(self.frame, text="Valide Contraseña: ")
        self.password_2_entry = tk.Entry(self.frame, textvariable=self.password_verification)
        
        self.rol_lbl = tk.Label(self.frame, text="Tipo de Usuario")
        self.rol_combobox = tk.OptionMenu(self.frame, self.rol_filter, *USER_TYPE_LIST, command=self.display_rol_frame)
        self.rol_frame = tk.Frame(self.frame)
        self.create_btn = tk.Button(self.frame, text="Crear Usuario", command=self.toplevel.destroy)
        
        self.first_name_lbl.grid(row=0, column=0, sticky="nw")
        self.first_name_entry.grid(row=0, column=1, sticky="nw")
        self.last_name_lbl.grid(row=1, column=0, sticky="nw")
        self.last_name_entry.grid(row=1, column=1, sticky="nw")
        self.id_lbl.grid(row=2, column=0, sticky="nw")
        self.id_entry.grid(row=2, column=1, sticky="nw")
        
        self.password_lbl.grid(row=3, column=0, sticky="nw")
        self.password_entry.grid(row=3, column=1, sticky="nw")    
        self.password_2_lbl.grid(row=4, column=0, sticky="nw")
        self.password_2_entry.grid(row=4, column=1, sticky="nw")
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
        
    def show(self):
        self.toplevel.grab_set()  # Block events in other windows
        self.toplevel.wait_window()  # Wait until the dialog is closed
        return self.add_usr()
    
    def add_usr(self):       
        if self.password.get() != self.password_verification.get():
            messagebox.showerror("Password Error", "Las contraseñas no coinciden")
            return
        
        email = f'{self.first_name.get().replace(" ", "")}{self.last_name.get().replace(" ", "")}{USTA_DOMAIN}'.lower()
        person = Tomasino(self.first_name.get(), self.last_name.get(), self.id.get(), self.cod, email, self.password.get())
        
        selection = self.rol_filter.get()
        print(self.rol_frame.children)
        if selection == "Estudiante":
            ## Create Student
            subjects = self.rol_frame_child._subjects
            semestre = self.rol_frame_child.semester.get()
            person = Estudiante(subjects, semestre, tomasino=person)
        elif selection == "Profesor":
            job = self.rol_frame_child.job.get()
            department = self.rol_frame_child.department.get()
            base_salary = self.rol_frame_child.base_salary.get()
            subjects = self.rol_frame_child._subjects
            person = Profesor(tomasino=person, job=job, department=department,
                              base_salary=base_salary, subjects=subjects)
        else:
            job = self.rol_frame_child.job.get()
            department = self.rol_frame_child.department.get()
            base_salary = self.rol_frame_child.base_salary.get()
            person = Administrativo(tomasino=person, 
                              job=job, department=department, base_salary=base_salary)
            
    # "Administrativo": lambda frame: FrameAdmin(frame),
    # "Profesor": lambda frame: FrameProfessor(frame)
        messagebox.showinfo("Operacion exitosa", f"{selection} creado")
        return person
    
        
        
        
        