# controllers/productos_controller.py
from helpers.breadcrumbs_static import get_productos_breadcrumb, get_categorias_breadcrumb, get_detalle_producto_breadcrumb


def productos(request):
    """
    Pantalla 1: Lista de productos
    Breadcrumb: Inicio > Productos
    """
    
    # Breadcrumb estático
    breadcrumb_html = get_productos_breadcrumb()
    
    # Productos de ejemplo
    productos_list = [
        {"id": 1, "nombre": "Electrónica", "descripcion": "Laptops, celulares, tablets", "icon": "💻", "count": 45},
     ]
    
    # Generar HTML de productos
    productos_html = ""
    for producto in productos_list:
        productos_html += f'''
        <div class="col-md-6 col-lg-4 mb-4">
            <a href="/categorias/{producto['id']}" class="category-card">
                <div class="category-icon">{producto['icon']}</div>
                <h3 class="category-title">{producto['nombre']}</h3>
                <p class="category-description">{producto['descripcion']}</p>
                <div class="category-count">{producto['count']} productos</div>
            </a>
        </div>
        '''
    
    # Leer template
    with open("templates/productos.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Reemplazar variables
    html = html.replace("{{breadcrumb_html}}", breadcrumb_html)
    html = html.replace("{{productos_list}}", productos_html)
    
    return html


def categorias(request):
    """
    Pantalla 2: Productos de una categoría
    Breadcrumb: Inicio > Productos > Categoría
    """
    
    # Obtener ID de categoría desde la URL (ejemplo)
    # categoria_id = request.path.split('/')[-1]
    categoria_id = "1"
    categoria_nombre = "Electrónica"
    
    # Breadcrumb estático con parámetros
    breadcrumb_html = get_categorias_breadcrumb(categoria_id, categoria_nombre)
    
    # Productos de la categoría
    items = [
        {"id": 101, "nombre": "Laptop Dell Inspiron", "precio": "$15,999", "imagen": "💻"},
    ]
    
    # Generar HTML de items
    items_html = ""
    for item in items:
        items_html += f'''
        <div class="col-md-6 col-lg-4 mb-4">
            <a href="/producto/{item['id']}" class="product-card">
                <div class="product-image">{item['imagen']}</div>
                <div class="product-info">
                    <h4 class="product-name">{item['nombre']}</h4>
                    <p class="product-price">{item['precio']}</p>
                    <button class="btn-ver-detalle">Ver detalles</button>
                </div>
            </a>
        </div>
        '''
    
    # Leer template
    with open("templates/categorias.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Reemplazar variables
    html = html.replace("{{breadcrumb_html}}", breadcrumb_html)
    html = html.replace("{{categoria_nombre}}", categoria_nombre)
    html = html.replace("{{items_html}}", items_html)
    
    return html


def detalle_producto(request):
    """
    Pantalla 3: Detalle de un producto
    Breadcrumb: Inicio > Productos > Categoría > Producto
    """
    
    # Obtener IDs desde la URL (ejemplo)
    producto_id = "101"
    categoria_id = "1"
    categoria_nombre = "Electrónica"
    
    # Datos del producto
    producto = {
        "id": 101,
        "nombre": "Laptop Dell Inspiron 15",
        "precio": "$15,999",
        "descripcion": "Laptop potente para trabajo y entretenimiento. Procesador Intel Core i7, 16GB RAM, 512GB SSD.",
        "caracteristicas": [
            "Procesador Intel Core i7 11va Gen",
            "16GB RAM DDR4",
            "512GB SSD NVMe",
            "Pantalla 15.6\" FHD",
            "Tarjeta gráfica NVIDIA MX450",
            "Windows 11 Pro"
        ],
        "imagen": "💻",
        "stock": 15,
        "categoria": categoria_nombre
    }
    
    # Breadcrumb estático con todos los parámetros
    breadcrumb_html = get_detalle_producto_breadcrumb(
        categoria_id, 
        categoria_nombre, 
        producto_id, 
        producto["nombre"]
    )
    
    # Generar HTML de características
    caracteristicas_html = ""
    for caract in producto["caracteristicas"]:
        caracteristicas_html += f'<li class="caracteristica-item">✓ {caract}</li>'
    
    # Leer template
    with open("templates/detalle-producto.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Reemplazar variables
    html = html.replace("{{breadcrumb_html}}", breadcrumb_html)
    html = html.replace("{{producto_nombre}}", producto["nombre"])
    html = html.replace("{{producto_precio}}", producto["precio"])
    html = html.replace("{{producto_descripcion}}", producto["descripcion"])
    html = html.replace("{{producto_imagen}}", producto["imagen"])
    html = html.replace("{{producto_stock}}", str(producto["stock"]))
    html = html.replace("{{caracteristicas_html}}", caracteristicas_html)
    
    return html