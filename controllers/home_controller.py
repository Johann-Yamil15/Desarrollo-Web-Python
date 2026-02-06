from core.render import render_view
from services.db_service import get_home_data


def index_action(breadcrumbs):
    # 1. Obtener datos a través del servicio
    datos_bd = get_home_data()
    

    context = {
        "titulo": "Monitor de Sistema",
        "mensaje": "Estado de infraestructura en tiempo real",
        "servidor_fecha": datos_bd['fecha_bd'],
        "Estado": "Activo" if datos_bd.get('online') else "Desactivado",
        "breadcrumbs": breadcrumbs
    }
    return render_view('home/index.html', context)