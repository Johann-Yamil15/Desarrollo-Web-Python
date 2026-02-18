import json
from datetime import datetime, date
from urllib.parse import parse_qs
from core.render import render_view
from services.user_service import UserService
# IMPORTA TU FUNCIÓN DE VALIDACIÓN
from utils.validators import validate_form


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def user_manager_action(breadcrumbs):
    return render_view('users/usuario.html', {"titulo": "Gestión de Usuarios", "breadcrumbs": breadcrumbs})


def user_api_dispatcher(environ, method):
    query_params = parse_qs(environ.get('QUERY_STRING', ''))
    user_id_url = query_params.get('id', [None])[0]

    try:
        # --- MÉTODO GET ---
        if method == 'GET':
            if user_id_url:
                data = UserService.get_user_by_id(user_id_url)
            else:
                data = UserService.get_all_users()
            return json.dumps(data, default=json_serial).encode('utf-8')

        # --- LECTURA DEL CUERPO (PARA POST, PUT, DELETE) ---
        length = int(environ.get('CONTENT_LENGTH', 0))
        raw_body = environ['wsgi.input'].read(length).decode('utf-8') if length > 0 else "{}"
        body = json.loads(raw_body)

        # --- VALIDACIÓN PREVIA (POST Y PUT) ---
        if method in ['POST', 'PUT']:
            errores = validate_form(body)
            if errores:
                return json.dumps({
                    "success": False,
                    "errors": errores,
                    "msg": "Corrija los errores en el formulario"
                }).encode('utf-8')

        # --- POST: CREAR ---
        if method == 'POST':
            success, message = UserService.register_user(body)
            if not success:
                errors = {"email": message} if "correo" in message.lower() else {}
                return json.dumps({
                    "success": False,
                    "errors": errors,
                    "msg": message
                }).encode('utf-8')
            return json.dumps({"success": True, "msg": message}).encode('utf-8')

        # --- PUT: ACTUALIZAR ---
        if method == 'PUT':
            # CORRECCIÓN: Ahora desempaquetamos AMBOS valores que envía el Service
            success, message = UserService.update_existing_user(body)
            return json.dumps({
                "success": success,
                "msg": message
            }).encode('utf-8')

        # --- DELETE: ELIMINAR ---
        if method == 'DELETE':
            user_id = body.get('id')
            # CORRECCIÓN: Recibimos la tupla para evitar errores de desempaquetado
            success, message = UserService.delete_user(user_id)
            return json.dumps({
                "success": success,
                "msg": message
            }).encode('utf-8')

    except Exception as e:
        # Este bloque atrapa cualquier error inesperado y evita que el JS se quede colgado
        return json.dumps({
            "success": False, 
            "msg": f"Error interno en servidor: {str(e)}"
        }).encode('utf-8')