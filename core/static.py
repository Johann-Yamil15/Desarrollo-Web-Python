import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

def serve_static(environ):
    path = environ.get("PATH_INFO", "")

    if not path.startswith("/static/"):
        return None

    file_path = path.replace("/static/", "")
    full_path = os.path.join(STATIC_DIR, file_path)

    if not os.path.isfile(full_path):
        return ("404 Not Found", b"Not Found", [])

    with open(full_path, "rb") as f:
        content = f.read()

    headers = [
        ("Content-Type", "text/css"),
        ("Content-Length", str(len(content)))
    ]

    return ("200 OK", content, headers)
