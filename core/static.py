import os
import mimetypes

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

def serve_static(environ):
    path = environ.get("PATH_INFO", "")

    if not path.startswith("/static/"):
        return None

    file_path = path.replace("/static/", "").lstrip("/") # Limpiamos barras extras
    full_path = os.path.join(STATIC_DIR, file_path)

    # Seguridad: Evitar que salgan de la carpeta static con ../
    if not os.path.abspath(full_path).startswith(os.path.abspath(STATIC_DIR)):
        return ("403 Forbidden", b"Acceso denegado", [])

    if not os.path.isfile(full_path):
        return ("404 Not Found", b"Archivo no encontrado", [])

    # Adivinar el tipo de contenido (image/jpeg, text/css, etc.)
    content_type, _ = mimetypes.guess_type(full_path)
    content_type = content_type or "application/octet-stream"

    with open(full_path, "rb") as f:
        content = f.read()

    headers = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(content)))
    ]

    return ("200 OK", content, headers)