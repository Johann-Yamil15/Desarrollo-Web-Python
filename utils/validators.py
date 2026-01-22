import re
from datetime import datetime

def validate_form(data):
    errors = {}

    # Nombre: Permite letras y espacios
    name = data.get("name", "").strip()
    if not name or not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", name):
        errors["name"] = "Usa solo letras y espacios"

    # Usuario: Alfanumérico sin espacios
    username = data.get("username", "")
    if len(username) < 5:
        errors["username"] = "Debe tener al menos 5 caracteres"
    elif not username.isalnum():
        errors["username"] = "Solo letras y números (sin espacios)"

    # Edad: Rango lógico
    age = data.get("age", "")
    if not age.isdigit():
        errors["age"] = "Ingresa un número válido"
    elif not (0 < int(age) < 120):
        errors["age"] = "Edad fuera de rango (1-119)"

    # Correo
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, data.get("email", "")):
        errors["email"] = "Formato de correo inválido"

    # Teléfono
    if not re.match(r"^\d{10}$", data.get("phone", "")):
        errors["phone"] = "Deben ser exactamente 10 dígitos"

    # Fecha: No permitir fechas futuras
    birthdate_str = data.get("birthdate", "")
    if not birthdate_str:
        errors["birthdate"] = "La fecha es obligatoria"
    else:
        try:
            birth_date = datetime.strptime(birthdate_str, "%Y-%m-%d")
            year_now = datetime.now().year
            
            # Validar que no sea en el futuro
            if birth_date > datetime.now():
                errors["birthdate"] = "No puedes haber nacido en el futuro"
            
            # Validar rango lógico (Mínimo año 1900)
            elif birth_date.year < 1900:
                errors["birthdate"] = f"El año {birth_date.year} es demasiado antiguo"
            
            # Validar edad mínima (ejemplo: 13 años)
            # edad = year_now - birth_date.year
            # if edad < 13:
            #    errors["birthdate"] = "Debes tener al menos 13 años"

        except ValueError:
            errors["birthdate"] = "Formato de fecha inválido"

    # Checkbox
    if "terms" not in data:
        errors["terms"] = "Debes aceptar para continuar"

    return errors