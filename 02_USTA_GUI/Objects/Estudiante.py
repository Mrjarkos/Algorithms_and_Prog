from Objects.Tomasino import Tomasino

class Estudiante(Tomasino):
    
    semester : int
    _subjects : list
    _grades : dict
    
    def __init__(self, subjects, semestre, tomasino: Tomasino):
        super().__init__(tomasino.first_name, tomasino.last_name, tomasino.id, tomasino.cod, tomasino.email, tomasino._password)
        self._subjects = subjects
        self.semester = semestre
        self._grades = {}
    
    def enroll_subject(self, subject):
        if len(self._subjects) >=8:
            errmsg = "OverloadException: El estudiante ya tiene demasiadas asignaturas"
            return errmsg
        self._subjects.append(subject)
        
    def list_grades(self, academic_period):
        result = self.validate_academic_period(academic_period)
        if not result[0]:
            return None

        return self._grades[academic_period]
            
    def get_averrage(self, academic_period=None):
        sume = 0
        n_subjects = 0
        
        ### Calculate total if no special academic_period
        periods = [academic_period] if academic_period else self._grades
            
        for period in periods:
            for grade in self._grades[period].values():
                ## TO DO: si el estudiante repite
                sume += grade
                n_subjects+=1
        return sume/n_subjects
        
    def validate_academic_period(self, academic_period):
        if academic_period not in self._grades:
            errmsg = f"ValueException: El estudiante no ha cursado en el periodo academico {academic_period}"
            print(errmsg)
            return False
        return True