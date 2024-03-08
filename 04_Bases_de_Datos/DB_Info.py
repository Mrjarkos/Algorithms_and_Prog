
from utils import common_keys

# Connection String
conn_dict = {
    "HOST": 'localhost',
    "DATABASE" : 'universidad',
    "USER" : 'postgres',
    "PASSWORD" : '0077'
}

materias : dict[str, tuple] = {
    "Derecho": (
        "Filosofía Institucional",
        "Antropología",
        "Inglés I",
        "Analítica I",
        "Introducción al Derecho",
        "Filosofía y Teoría del Derecho",
        "Sociología Jurídica",
        "Historia del Derecho"
    ),
    "Ingenieria": (
        "Física Mecánica y Termodinámica",
        "Álgebra Lineal",
        "Cálculo Diferencial",
        "Fundamentos de Circuitos",
        "Introducción a la Ingeniería",
        "Filosofía Institucional",
        "Cátedra Henri Didon"
    ),
    "Humanidades": (
        "Introducción al Mundo Moderno",
        "Pensamiento Lógico",
        "Lengua Extranjera – Inglés I",
        "Filosofía Institucional",
        "Cátedra Henri Didon",
        "Investigación I: Epistemología y Paradigmas",
        "Fundamentos del Pensamiento Sociológico"
    )
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
    },
    "materias" : {
        "id" : int,
        "nombre" : str,
        "facultad" : str
    },
    "materias_estudiantes" : {
        "id" : int,
        "materia_id": int,
        "estudiante_id": int,
        "docente_id": int
    }
}

COMMON_ATTRB : list[str] = common_keys(tables["estudiantes"], tables["docentes"])