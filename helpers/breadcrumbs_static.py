# helpers/breadcrumbs_static.py
"""
Helper para generar breadcrumbs estáticos
Para rutas específicas con jerarquía predefinida
"""

def render_breadcrumb(items):
    """
    Genera el HTML del breadcrumb a partir de una lista de items
    
    Args:
        items (list): Lista de diccionarios con estructura:
            [
                {"title": "Inicio", "icon": "🏠", "url": "/", "active": False},
                {"title": "Productos", "icon": "📦", "url": "/productos", "active": True}
            ]
    
    Returns:
        str: HTML del breadcrumb
    """
    if not items:
        return ""
    
    html_parts = ['<nav class="breadcrumb-nav" aria-label="breadcrumb">']
    html_parts.append('  <ol class="breadcrumb">')
    
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1) or item.get("active", False)
        
        if is_last:
            # Último elemento (activo)
            html_parts.append(f'    <li class="breadcrumb-item active" aria-current="page">')
            html_parts.append(f'      <span class="breadcrumb-icon">{item["icon"]}</span>')
            html_parts.append(f'      <span>{item["title"]}</span>')
            html_parts.append(f'    </li>')
        else:
            # Elementos con enlace
            html_parts.append(f'    <li class="breadcrumb-item">')
            html_parts.append(f'      <a href="{item["url"]}">')
            html_parts.append(f'        <span class="breadcrumb-icon">{item["icon"]}</span>')
            html_parts.append(f'        <span>{item["title"]}</span>')
            html_parts.append(f'      </a>')
            html_parts.append(f'    </li>')
    
    html_parts.append('  </ol>')
    html_parts.append('</nav>')
    
    return '\n'.join(html_parts)


# ============================================
# BREADCRUMBS PREDEFINIDOS PARA CADA PANTALLA
# ============================================

def get_productos_breadcrumb():
    """Breadcrumb para la pantalla de Productos"""
    items = [
        {
            "title": "Inicio",
            "icon": "🏠",
            "url": "/",
            "active": False
        },
        {
            "title": "Productos",
            "icon": "📦",
            "url": "/productos",
            "active": True
        }
    ]
    return render_breadcrumb(items)


def get_categorias_breadcrumb(categoria_id=None, categoria_nombre="Electrónica"):
    """Breadcrumb para la pantalla de Categorías"""
    items = [
        {
            "title": "Inicio",
            "icon": "🏠",
            "url": "/",
            "active": False
        },
        {
            "title": "Productos",
            "icon": "📦",
            "url": "/productos",
            "active": False
        },
        {
            "title": categoria_nombre,
            "icon": "🏷️",
            "url": f"/categorias/{categoria_id}" if categoria_id else "/categorias",
            "active": True
        }
    ]
    return render_breadcrumb(items)


def get_detalle_producto_breadcrumb(categoria_id="1", categoria_nombre="Electrónica", 
                                    producto_id="101", producto_nombre="Laptop Dell"):
    """Breadcrumb para la pantalla de Detalle del Producto"""
    items = [
        {
            "title": "Inicio",
            "icon": "🏠",
            "url": "/",
            "active": False
        },
        {
            "title": "Productos",
            "icon": "📦",
            "url": "/productos",
            "active": False
        },
        {
            "title": categoria_nombre,
            "icon": "🏷️",
            "url": f"/categorias/{categoria_id}",
            "active": False
        },
        {
            "title": producto_nombre,
            "icon": "🎯",
            "url": f"/producto/{producto_id}",
            "active": True
        }
    ]
    return render_breadcrumb(items)