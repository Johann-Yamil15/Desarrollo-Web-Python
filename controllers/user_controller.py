import json
from datetime import datetime, date
from urllib.parse import parse_qs
from core.render import render_view
from services.user_service import UserService 

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
        # GET - Usamos UserService
        if method == 'GET':
            if user_id_url:
                data = UserService.get_user_by_id(user_id_url)
            else:
                data = UserService.get_all_users()
            
            return json.dumps(data, default=json_serial).encode('utf-8')

        # Procesar Body para POST/PUT/DELETE
        length = int(environ.get('CONTENT_LENGTH', 0))
        raw_body = environ['wsgi.input'].read(length).decode('utf-8') if length > 0 else "{}"
        body = json.loads(raw_body)

        # POST - Crear
        if method == 'POST':
            success = UserService.register_user(body)
            return json.dumps({"success": success, "msg": "Usuario creado" if success else "Error al crear"}).encode('utf-8')

        # PUT - Actualizar
        if method == 'PUT':
            # Llamamos al nuevo método del servicio
            success = UserService.update_existing_user(body)
            return json.dumps({"success": success, "msg": "Actualizado correctamente" if success else "Error"}).encode('utf-8')

        # DELETE - Eliminar
        if method == 'DELETE':
            user_id = body.get('id')
            success = UserService.delete_user(user_id)
            return json.dumps({"success": success, "msg": "Eliminado"}).encode('utf-8')

    except Exception as e:
        return json.dumps({"success": False, "msg": f"Error en servidor: {str(e)}"}).encode('utf-8')