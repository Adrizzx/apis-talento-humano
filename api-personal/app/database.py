import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    """Obtiene una conexión a la base de datos PostgreSQL"""
    try:
        # Usar DATABASE_URL completa (funciona tanto en Render como en local)
        conn = psycopg2.connect(
            Config.DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise e

def close_db_connection(conn):
    """Cierra la conexión a la base de datos"""
    if conn:
        conn.close()