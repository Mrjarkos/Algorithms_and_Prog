
# ! Warning
# * Este script solo se ejecuta una sola vez para la creacion de la base de datos

import psycopg2
import sys
import os
 

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from db_conf import *

#Conectarse al servidor de "PostgreSQL 16" / database default
conn = psycopg2.connect(
    host=HOST,
    database="postgres",
    user=USER,
    password=PASSWORD
)

cur = conn.cursor()

# !Deshabilita la autocommit para evitar el error de transacción
conn.autocommit = True
cur.execute("CREATE DATABASE blog;")

conn.close()

# Trabajar sobre blog
conn = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,    
    password=PASSWORD
)

cur = conn.cursor()

## Roles

cur.execute("CREATE TYPE rol_enum AS ENUM ('admin', 'user');")

# Crea la tabla "users"
cur.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        rol rol_enum
    );
""")

# Crea la tabla "Blogs"
cur.execute("""
    CREATE TABLE blogs (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        summary VARCHAR(255),
        post TEXT,
        slug VARCHAR(255),
        cover VARCHAR(255),
        author INTEGER REFERENCES users(id),    
        added TIMESTAMP DEFAULT current_timestamp,
        edited TIMESTAMP DEFAULT current_timestamp
    );
""")

# Confirma los cambios y cierra la conexión
conn.commit()
conn.close()