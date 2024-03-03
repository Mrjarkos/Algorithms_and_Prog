
from utils import common_keys

# Connection String
conn_dict = {
    "HOST": 'localhost',
    "DATABASE" : 'universidad',
    "USER" : 'postgres',
    "PASSWORD" : '0077'
}

tables = {
    "estudiantes" : {
        "id" : int,
        "nombre" : str,
        "identificacion" : str,
        "edad" : int,
        "semestre" : int,
        "carrera" : str,
        "facultad" : str
    }, 
    "docentes" : {
        "id" : int,
        "nombre" : str,
        "identificacion" : str,
        "edad" : int,
        "especialidad" : str,
        "facultad" : str
    }
}

COMMON_ATTRB : list[str] = common_keys(tables["estudiantes"], tables["docentes"])