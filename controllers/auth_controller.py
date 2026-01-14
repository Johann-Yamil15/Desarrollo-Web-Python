from config.database import get_connection
from services.user_service import hash_password
from core.response import Response
from datetime import datetime

# Registration controller
def register(request):
    if request.method == "GET":
        return open("views/register.html", encoding="utf-8").read()

    data = request.form()

    # Validar campos
    nombre = data.get("nombre")
    ap = data.get("apellido_p")
    am = data.get("apellido_m")
    email = data.get("email")
    fecha_nac_str = data.get("fecha_nacimiento")
    password = data.get("password")

    if not all([nombre, ap, am, email, fecha_nac_str, password]):
        return "<h3>Error: Todos los campos son obligatorios</h3>"

    # Convertir fecha a datetime
    try:
        fecha_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d")
    except ValueError:
        return "<h3>Error: Formato de fecha inválido</h3>"

    # Hash de contraseña
    password_hash = hash_password(password)

    # Insertar en la base de datos
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Usuarios
            (Nombre, ApellidoP, ApellidoM, Email, FechaNacimiento, PasswordHash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, ap, am, email, fecha_nac, password_hash))

        conn.commit()
        cursor.close()
        conn.close()

        return "<h2>Registro exitoso</h2><a href='/login'>Iniciar sesión</a>"

    except Exception as e:
        return f"<h3>Error al registrar:</h3><pre>{e}</pre>"


# Login controller
def login(request):
    if request.method == "GET":
        return open("views/login.html", encoding="utf-8").read()

    data = request.form()
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Id, PasswordHash FROM Usuarios WHERE Email = ?", email
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return "<h3>Usuario no encontrado</h3>"

    if not verify_password(password, user.PasswordHash):
        return "<h3>Contraseña incorrecta</h3>"

    return "<h2>Login exitoso</h2>"
