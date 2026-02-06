import os
import mimetypes
from core.render import render_view
from core.router import get_route_handler 

def get_breadcrumbs(path):
    parts = [p for p in path.split('/') if p]
    breadcrumbs = [{"name": "My Project", "url": "/"}]
    current_url = ""
    for part in parts:
        current_url += f"/{part}"
        name = part.replace('_', ' ').replace('-', ' ').title()
        breadcrumbs.append({"name": name, "url": current_url})
    return breadcrumbs

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    if path == '/favicon.ico':
        start_response('204 No Content', [('Content-Length', '0')])
        return [b""]

    # --- 1. LÓGICA PARA ARCHIVOS ESTÁTICOS ---
    if path.startswith('/static/'):
        file_path = os.path.join(os.getcwd(), path.lstrip('/'))
        if os.path.exists(file_path):
            if file_path.endswith(".css"): content_type = "text/css"
            elif file_path.endswith(".js"): content_type = "application/javascript"
            else:
                content_type, _ = mimetypes.guess_type(file_path)
                if not content_type: content_type = "text/plain"

            start_response('200 OK', [('Content-Type', content_type)])
            with open(file_path, 'rb') as f: return [f.read()]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b"Archivo estatico no encontrado"]

    # --- 2. PROCESAMIENTO DE RUTAS DINÁMICAS ---
    breadcrumbs = get_breadcrumbs(path)
    handler, status = get_route_handler(path, method)

    ctype = 'text/html; charset=utf-8'
    if path.startswith('/api/'):
        ctype = 'application/json'
    
    headers = [('Content-type', ctype)]

    # --- CAMBIO CLAVE AQUÍ ---
    # Pasamos siempre breadcrumbs y environ a todos los handlers.
    # El Router se encargará de decidir cuáles usa cada controlador.
    try:
        if status == '404 Not Found':
            # El 404 suele recibir bc y el path errado
            response_body = handler(breadcrumbs, path)
        else:
            # Para Carrusel, Usuarios y API, enviamos ambos
            response_body = handler(breadcrumbs, environ)
            
        # Aseguramos que la respuesta sea bytes
        if isinstance(response_body, str):
            response_body = response_body.encode('utf-8')
            
    except Exception as e:
        print(f"🔥 Error ejecutando handler: {e}")
        status = '500 Internal Server Error'
        response_body = f"Error crítico en el servidor: {e}".encode('utf-8')

    start_response(status, headers)
    return [response_body]