import psycopg2
from psycopg2 import pool
from flask import g, current_app

# Configuración de la conexión a PostgreSQL
db_config = {
    'dbname': 'bank_db',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

# Crear un pool de conexiones con más conexiones disponibles
connection_pool = pool.SimpleConnectionPool(1, 20, **db_config)

def get_db():
    if 'db' not in g:
        g.db = connection_pool.getconn()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        connection_pool.putconn(db)

def init_app(app):
    # Registrar la función close_db para ejecutarse al finalizar cada solicitud
    app.teardown_appcontext(close_db)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Leer el esquema SQL desde el archivo
        with open('schema.sql', 'r') as f:
            schema = f.read()
        
        # Ejecutar el esquema SQL
        cursor.execute(schema)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        cursor.close()