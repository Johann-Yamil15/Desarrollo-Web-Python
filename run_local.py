from wsgiref.simple_server import make_server
from app import application

if __name__ == "__main__":
    print("Servidor WSGI local activo en http://localhost:8000")
    make_server("", 8000, application).serve_forever()
