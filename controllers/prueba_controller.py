from config.database import get_connection
from services.user_service import hash_password
from datetime import datetime

def prueba(request):
    if request.method == "GET":
        return open("views/prueba.html", encoding="utf-8").read()

    # DATOS ESTÁTICOS
    nombre = "Juan"
    ap = "Pérez"
    am = "Gómez"
    email = f"usuario{datetime.now().strftime('%f')}@test.com"
    fecha_nac = datetime(1990, 1, 1)
    password_hash = hash_password("123456")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Usuarios
            (Nombre, ApellidoP, ApellidoM, Email, FechaNacimiento, PasswordHash)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nombre,
            ap,
            am,
            email,
            fecha_nac,
            password_hash
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return "<h2>✔ Usuario agregado correctamente</h2><a href='/'>Volver</a>"

    except Exception as e:
        return f"<h3>Error:</h3><pre>{e}</pre>"
