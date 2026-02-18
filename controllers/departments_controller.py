import json
from urllib.parse import parse_qs
from core.render import render_view
from services.department_service import DepartmentService
from datetime import datetime, date

def json_serial(obj):
    """Serializador para objetos datetime/date que JSON no soporta por defecto"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def department_manager_action(breadcrumbs):
    """Renderiza la nueva interfaz de gestión de departamentos"""
    return render_view('users/departments.html', {
        "titulo": "Gestión de Departamentos y Permisos", 
        "breadcrumbs": breadcrumbs
    })

def department_api_dispatcher(environ, method):
    """Maneja el CRUD completo de /api/departments"""
    try:
        # --- MÉTODO GET: Listar todos ---
        if method == 'GET':
            data = DepartmentService.get_all_departments()
            return json.dumps(data, default=json_serial).encode('utf-8')

        # Para POST, PUT y DELETE necesitamos leer el cuerpo (body)
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            data = json.loads(request_body) if request_body else {}
        except:
            data = {}

        # --- MÉTODO POST: Crear ---
        if method == 'POST':
            success, msg = DepartmentService.add_department(data)
            return json.dumps({"success": success, "msg": msg}).encode('utf-8')

        # --- MÉTODO PUT: Actualizar ---
        elif method == 'PUT':
            depto_id = data.get('id')
            if not depto_id:
                return json.dumps({"success": False, "msg": "ID requerido"}).encode('utf-8')
            
            success, msg = DepartmentService.update_department(depto_id, data)
            return json.dumps({"success": success, "msg": msg}).encode('utf-8')

        # --- MÉTODO DELETE: Eliminar ---
        elif method == 'DELETE':
            depto_id = data.get('id')
            if not depto_id:
                return json.dumps({"success": False, "msg": "ID requerido"}).encode('utf-8')

            success, msg = DepartmentService.delete_department(depto_id)
            return json.dumps({"success": success, "msg": msg}).encode('utf-8')

        return json.dumps({"success": False, "msg": "Método no permitido"}).encode('utf-8')

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        return json.dumps({
            "success": False,
            "msg": f"Error en API: {str(e)}"
        }).encode('utf-8')