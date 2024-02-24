from Objects.Tomasino import Tomasino
from Objects.Empleado import Empleado

class Administrativo(Empleado):
    
    def __init__(self, tomasino: Tomasino, job, department, base_salary):
        super().__init__(tomasino, job, department, base_salary)
    
    ## A los administrativos se les paga por dias
    def calculate_salary(self, days_worked : int):
        return self.base_salary * days_worked
    
    def issue_certificate(self, certificate, tomasino: Tomasino):
        print(f"""La USTA certifica que {tomasino.first_name} {tomasino.last_name},
              identificado con {tomasino.id_type} No. {tomasino.id} esta vinculado
              a esta universidad""")