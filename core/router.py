# routes.py
from controllers.home_controller import home
from controllers.auth_controller import login, register
from controllers.prueba_controller import prueba
from controllers.error_controller import error
from controllers.form_controller import form_test
from controllers.carousel_controller import carrusel
from controllers.productos_controller import productos, categorias, detalle_producto


routes = {
    # Home
    ("GET", "/"): home, 
    ("POST", "/"): home, 
    
    # Prueba
    ("GET", "/prueba"): prueba,
    ("POST", "/prueba"): prueba,
    
    # Carrusel
    ("GET", "/carrusel"): carrusel,
    ("POST", "/carrusel"): carrusel,
    
    # Formulario de validaciones (SIN DB)
    ("GET", "/form-test"): form_test,
    ("POST", "/form-test"): form_test,
    
    # Error 404
    ("GET", "/404"): error,
    
    # Login
    ("GET", "/login"): login,
    ("POST", "/login"): login,
    
    # Register
    ("GET", "/register"): register,
    ("POST", "/register"): register,
    
    # ============================================
    # PRODUCTOS - Sistema de Breadcrumbs Estáticos
    # ============================================
    
    # Pantalla 1: Lista de categorías de productos
    # Breadcrumb: Inicio > Productos
    ("GET", "/productos"): productos,
    
    # Pantalla 2: Productos de categorías específicas
    # Breadcrumb: Inicio > Productos > [Categoría]
    ("GET", "/categorias/1"): categorias,  # Electrónica
    ("GET", "/categorias/2"): categorias,  # Ropa
    ("GET", "/categorias/3"): categorias,  # Hogar
    ("GET", "/categorias/4"): categorias,  # Deportes
    ("GET", "/categorias/5"): categorias,  # Libros
    ("GET", "/categorias/6"): categorias,  # Juguetes
    
    # Pantalla 3: Detalle de productos específicos
    # Breadcrumb: Inicio > Productos > [Categoría] > [Producto]
    ("GET", "/producto/101"): detalle_producto,  # Laptop Dell
    ("GET", "/producto/102"): detalle_producto,  # iPhone 15 Pro
    ("GET", "/producto/103"): detalle_producto,  # iPad Air
    ("GET", "/producto/104"): detalle_producto,  # AirPods Pro
    ("GET", "/producto/105"): detalle_producto,  # Apple Watch
    ("GET", "/producto/106"): detalle_producto,  # MacBook Pro
}

def resolve(request):
    """
    Resuelve la ruta y retorna el controller correspondiente
    
    Args:
        request: Objeto con 'method' y 'path'
    
    Returns:
        function: Controller function o None
    """
    return routes.get((request.method, request.path))