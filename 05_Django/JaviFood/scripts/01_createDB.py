
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

# Confirma los cambios y cierra la conexión
conn.commit()
conn.close()