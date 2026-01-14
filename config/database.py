import pyodbc
from config.settings import DB_CONN

def get_connection():
    return pyodbc.connect(DB_CONN)

def test_connection():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT GETDATE()")
    fecha = cursor.fetchone()[0]
    conn.close()
    return fecha
