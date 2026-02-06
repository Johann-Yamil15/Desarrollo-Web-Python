import os
from core.render import render_view
from services.carrusel_service import CarruselService
from werkzeug.wrappers import Request

def carrusel_controller(breadcrumbs, env=None):
    # Validamos que el entorno env haya llegado
    if env is None:
        return "<h3>Error: El entorno de red (WSGI env) no fue proporcionado.</h3>".encode('utf-8')

    request = Request(env)

    # --- MÉTODO GET: Mostrar la página ---
    if request.method == "GET":
        items_db = CarruselService.get_all_items()
        
        # Generamos el HTML de los items dinámicamente
        items_html = ""
        for i, item in enumerate(items_db):
            active = "active" if i == 0 else ""
            items_html += f"""
                <div class="carousel-item {active}">
                    <img src="{item['ruta_relativa']}" class="d-block w-100" alt="Imagen {i+1}">
                </div>
            """
        
        # Si no hay imágenes, mostrar un placeholder
        if not items_db:
            items_html = '<div class="carousel-item active"><img src="https://via.placeholder.com/1200x500?text=No+hay+imagenes+disponibles" class="d-block w-100"></div>'

        # Usamos render_view igual que en el controlador de usuarios
        # Pasamos 'items_carrusel' para que se reemplace en la vista
        return render_view('carrusel/carrusel.html', {
            "titulo": "Gestión de Carrusel",
            "breadcrumbs": breadcrumbs,
            "items_carrusel": items_html
        })

    # --- MÉTODO POST: Guardar imagen ---
    if request.method == "POST":
        file = request.files.get("imagen")
        success, msg = CarruselService.save_image(file)
        
        if success:
            # Respuesta con script para refrescar
            return f'<script>alert("{msg}"); window.location.href="/carrusel";</script>'.encode('utf-8')
        else:
            return f'<h3>Error: {msg}</h3><a href="/carrusel">Volver</a>'.encode('utf-8')