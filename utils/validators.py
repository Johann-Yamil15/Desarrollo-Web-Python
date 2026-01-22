import re
from datetime import datetime

def validate_form(data):
    errors = {}

    # Nombre: solo letras y espacios, 1–50 caracteres, no solo espacios
    name = data.get("name", "")
    name_clean = name.strip()

    if not name_clean:
        errors["name"] = "El nombre no puede estar vacío"
    elif len(name_clean) > 50:
        errors["name"] = "El nombre no debe exceder 50 caracteres"
    elif not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", name_clean):
        errors["name"] = "Usa solo letras y espacios"

    # Usuario: alfanumérico, 5–50 caracteres, sin espacios
    username = data.get("username", "")
    username_clean = username.strip()

    if not username_clean:
        errors["username"] = "El usuario no puede estar vacío"
    elif len(username_clean) < 5:
        errors["username"] = "Debe tener al menos 5 caracteres"
    elif len(username_clean) > 50:
        errors["username"] = "No debe exceder 50 caracteres"
    elif not username_clean.isalnum():
        errors["username"] = "Solo letras y números (sin espacios)"

    # Correo
    email = data.get("email", "")
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        errors["email"] = "Formato de correo inválido"

    # Teléfono: exactamente 10 dígitos
    phone = data.get("phone", "")
    if not re.fullmatch(r"\d{10}", phone):
        errors["phone"] = "Deben ser exactamente 10 dígitos"

    # Fecha de nacimiento
    birthdate_str = data.get("birthdate", "")
    if not birthdate_str:
        errors["birthdate"] = "La fecha es obligatoria"
    else:
        try:
            birth_date = datetime.strptime(birthdate_str, "%Y-%m-%d")

            if birth_date > datetime.now():
                errors["birthdate"] = "No puedes haber nacido en el futuro"
            elif birth_date.year < 1900:
                errors["birthdate"] = f"El año {birth_date.year} es demasiado antiguo"

        except ValueError:
            errors["birthdate"] = "Formato de fecha inválido"

    # Checkbox términos
    if not data.get("terms"):
        errors["terms"] = "Debes aceptar para continuar"

    return errors
