
# ! Warning
# * Este script solo se ejecuta una sola vez para la creacion de la base de datos
# req: Cree una base de datos llamada universidad y dentro de esta cree dos tablas llamadas estudiantes y otra docentes

import psycopg2

# TODO: No hard-code la contraseña
USER="postgres"
PASSWORD = "0077"

#Conectarse al servidor de "PostgreSQL 16" / database default
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user=USER,
    password=PASSWORD
)

cur = conn.cursor()

# !Deshabilita la autocommit para evitar el error de transacción
conn.autocommit = True
cur.execute("CREATE DATABASE universidad;")

conn.close()

# Trabajar sobre universidad
conn = psycopg2.connect(
    host="localhost",
    database="universidad",
    user=USER,    
    password=PASSWORD
)

cur = conn.cursor()

# Crea la tabla "estudiantes"
cur.execute("""
    CREATE TABLE estudiantes (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255),
        identificacion VARCHAR(255),
        edad INTEGER,
        semestre INTEGER,
        carrera VARCHAR(255),
        facultad VARCHAR(255)
    );
""")

# Crea la tabla "docentes"
cur.execute("""
    CREATE TABLE docentes (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255),
        identificacion VARCHAR(255),
        edad INTEGER,       
        facultad VARCHAR(255),
        especialidad VARCHAR(255)
    );
""")

# Crea la tabla "materias"
# req: cree una tabla Materias que se asocia con las tablas anteriores
cur.execute("""
    CREATE TABLE materias (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255),
        facultad VARCHAR(255)
    );
""")

cur.execute("""
    CREATE TABLE materias_estudiantes (
        id SERIAL PRIMARY KEY,
        materia_id  INTEGER REFERENCES materias(id),
        estudiante_id INTEGER REFERENCES estudiantes(id),
        docente_id INTEGER REFERENCES docentes(id)
    );
""")

# Confirma los cambios y cierra la conexión
conn.commit()
conn.close()

print("Se creó la base de datos 'universidad' con las tablas 'estudiantes', 'docentes' y materias.")
