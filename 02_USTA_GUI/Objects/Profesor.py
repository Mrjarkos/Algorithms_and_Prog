from Objects.Tomasino import Tomasino
from Objects.Empleado import Empleado

class Profesor(Empleado):
    
    _subjects : list
    
    def __init__(self, tomasino : Tomasino, job=None, department=None, base_salary=None, subjects=None ):
        super().__init__(tomasino, job, department, base_salary)
        self._subjects = subjects if subjects is not None else []
    
    ## A los profesores se les paga por horas
    def calculate_salary(self, hours_worked : float):
        days_worked = hours_worked/8
        return self.base_salary * days_worked
    
    def add_subject(self, subject : str):
        if len(self._subjects) >=3:
            errmsg = "OverloadException: El docente ya tiene demasiadas asignaturas"
            return errmsg
        self._subjects.append(subject)
        
    def grade(self, subject, student):
        raise NotImplementedError