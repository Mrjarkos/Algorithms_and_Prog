from pickle import NONE
import psycopg2
from psycopg2._psycopg import (
    connection,
    cursor
    )

from DB_Info import conn_dict, COMMON_ATTRB
import copy

class DBManager():
    
    def __init__(self) -> None:
        self.conn : connection = psycopg2.connect(
            host = conn_dict["HOST"],
            database = conn_dict["DATABASE"],
            user = conn_dict["USER"],
            password = conn_dict["PASSWORD"]
        )
        
        self.cur : cursor  = self.conn.cursor()
        self.conn.autocommit = False
    
    def validate_unique_ident(self, identificacion: str):
        regs = self.get_proff_students(filter={"identificacion": identificacion})
        return not any(any(k) for k in regs.values())
    
    def update_estudiante(self, nombre: str, identificacion: str, edad: int, semestre: int, 
                          carrera: str, facultad: str):
        props = "nombre = %s, edad = %s, semestre = %s, carrera = %s, facultad = %s"
        estudiante = (nombre, edad, semestre, carrera, facultad, identificacion,)
        self.cur.execute(f"""
                         UPDATE estudiantes SET {props} WHERE identificacion = %s;
                         """, estudiante)
        self.conn.commit()
        
        # TODO: Control de errores
        return True
    
    def update_profesor(self, nombre: str, identificacion: str, edad: int, 
                        facultad: str, especialidad: str) -> bool:
        props = "nombre = %s, edad = %s, facultad = %s, especialidad = %s"
        profesor = (nombre, edad, facultad, especialidad, identificacion)
        self.cur.execute(f"""
                         UPDATE docentes SET {props} WHERE identificacion = %s;
                         """, profesor)
        self.conn.commit()
        
        # TODO: Control de errores
        return True
    
    def insert_estudiante(self, nombre: str, identificacion: str, edad: int, semestre: int, 
                          carrera: str, facultad: str) -> bool:
        estudiante = (nombre, identificacion, edad, semestre, carrera, facultad)
        
        self.cur.execute("""
            INSERT INTO estudiantes (nombre, identificacion, edad, semestre, carrera, facultad)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, estudiante)
        self.conn.commit()
        
        # TODO: Control de errores
        return True
    
    def insert_profesor(self, nombre: str, identificacion: str, edad: int, 
                        facultad: str, especialidad: str) -> bool:
        profesor = (nombre, identificacion, edad, facultad, especialidad)
        self.cur.execute("""
            INSERT INTO docentes (nombre, identificacion, edad, facultad, especialidad)
            VALUES (%s, %s, %s, %s, %s);
        """, profesor)
        self.conn.commit()

        # TODO: Control de errores
        return True

    def get_estudiantes(self, properties : list[str] | None = None, filter : dict | None = None):
        prop = DBManager.generate_properties_query(properties)
        where = DBManager.generate_filter_query(filter)
        
        self.cur.execute(f"""
            SELECT {prop} FROM estudiantes {where}
            ORDER BY id ASC;
        """)
        return self.cur.fetchall()

    def get_profesores(self, properties : list[str] | None = None, filter : dict | None = None):
        prop = DBManager.generate_properties_query(properties)
        where = DBManager.generate_filter_query(filter)
            
        self.cur.execute(f"""
            SELECT {prop} FROM docentes {where}
            ORDER BY id ASC;
        """)
        return self.cur.fetchall()
    
    def get_proff_students(self, properties : list[str] | None = None, filter : dict | None = None):
        students = self.get_estudiantes(properties, filter)
        profes = self.get_profesores(properties, filter)
        return {"estudiante": students , "profesor" : profes}
    
    @staticmethod
    def generate_filter_query(filter : dict | None = None) -> str:
        where_query = ""
        if filter:
            where_query = "WHERE " + ", ".join([f"{pr} = '{val}'" for pr, val in filter.items()])
        return where_query
    
    @staticmethod
    def generate_properties_query(properties : list[str] | None = None) -> str:
        prop = copy.deepcopy(properties)
        if not prop:
            prop = ["*"]
        else:
            prop = DBManager.sort_properties(prop)
        return ", ".join(prop)
    
    @staticmethod
    def sort_properties(properties : list[str], exclude : list[str] | None = None):
        prop = copy.deepcopy(properties)
        ordered = ["identificacion", "nombre", "edad", "facultad"]
        sorted_prop = []
        for el in ordered:
            if el in properties:
                sorted_prop.append(el)
                prop.remove(el)
        prop.sort()
        lst = sorted_prop + prop
        if exclude:
            lst = [l for l in lst if l not in exclude]
        return lst
        
        
def main():
    ## Unit Testing
    dbmanager = DBManager()
    dbmanager.insert_estudiante("Javier", "1005042848", 11, 1, "Ing. Electronica", "Ing. Electronica")
    print(dbmanager.get_estudiantes())
    dbmanager.insert_profesor("Camilo", "504284885", 40, "Ing. Electronica", "Programacion")
    print(dbmanager.get_profesores())
    all = dbmanager.get_proff_students()
    print(all)
    
    unique = dbmanager.validate_unique_ident("504284885")
    print(unique)
    unique = dbmanager.validate_unique_ident("504284881")
    print(unique)
    
    dbmanager.update_estudiante("Javier", "1005042848", 20, 1, "Ing. Electronica", "Ing. Electronica")
    print(dbmanager.get_estudiantes())
    
    dbmanager.update_profesor("Camilo", "504284885", 42, "Ing. Electronica", "Programacion")
    print(dbmanager.get_profesores())
    
if __name__ == "__main__":
    main()