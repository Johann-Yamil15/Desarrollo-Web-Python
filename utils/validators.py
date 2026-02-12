import re
from datetime import datetime

def validate_form(data):
    errors = {}

    # --- NOMBRE ---
    nombre = data.get("nombre", "").strip()
    if not nombre:
        errors["nombre"] = "El nombre no puede estar vacío"
    elif not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", nombre):
        errors["nombre"] = "Usa solo letras y espacios"

    # --- APELLIDO PATERNO (ap) ---
    ap = data.get("ap", "").strip()
    if not ap:
        errors["ap"] = "El apellido paterno es obligatorio"
    elif not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", ap):
        errors["ap"] = "Usa solo letras y espacios"

    # --- APELLIDO MATERNO (am) ---
    am = data.get("am", "").strip()
    # El materno suele ser opcional, pero si escriben algo, validamos que sean letras
    if am and not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", am):
        errors["am"] = "Usa solo letras y espacios"

    # --- CORREO (INSTITUCIONAL Y MÚLTIPLES PUNTOS) ---
    email = data.get("email", "").strip()
    # Regex ajustada para permitir .edu.mx
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]{2,})+$"

    if not email:
        errors["email"] = "El correo es obligatorio"
    elif not re.fullmatch(email_regex, email):
        errors["email"] = "Formato inválido (ejemplo: usuario@uttt.edu.mx)"

    # --- FECHA DE NACIMIENTO ---
    fecha_nac_str = data.get("fecha_nac", "")
    if not fecha_nac_str:
        errors["fecha_nac"] = "La fecha es obligatoria"
    else:
        try:
            birth_date = datetime.strptime(fecha_nac_str, "%Y-%m-%d").date()
            today = datetime.now().date()

            if birth_date > today:
                errors["fecha_nac"] = "La fecha no puede ser futura"
            elif birth_date.year < 1900:
                errors["fecha_nac"] = "El año es demasiado antiguo"
        except ValueError:
            errors["fecha_nac"] = "Formato de fecha inválido"

    return errors