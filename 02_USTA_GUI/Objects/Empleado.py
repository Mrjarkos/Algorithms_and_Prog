from Objects.Tomasino import Tomasino
from abc import ABC, abstractmethod

class Empleado(Tomasino, ABC):
    
    job : str
    department : str
    base_salary : float
    
    def __init__(self, tomasino: Tomasino, job, department, base_salary):
        super().__init__(tomasino.first_name, tomasino.last_name, tomasino.id, tomasino.cod, tomasino.email, tomasino._password)
        self.job = job
        self.department = department
        self.base_salary = base_salary
    
    @abstractmethod
    def calculate_salary(self):
        pass
    
    