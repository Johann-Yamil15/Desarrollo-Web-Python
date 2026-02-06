from wsgiref.simple_server import make_server
from app import application  # Importa la función 'application' de tu app.py

if __name__ == "__main__":
    port = 8000
    print(f" Servidor de desarrollo activo en: http://localhost:{port}")
    
    # Creamos el servidor local
    httpd = make_server("localhost", port, application)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n Servidor detenido.")