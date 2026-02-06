from core.render import render_view

# IMPORTANTE: Debe recibir 'breadcrumbs' Y 'path_erroneo'
def not_found_action(breadcrumbs, path_erroneo):
    context = {
        "breadcrumbs": breadcrumbs,
        "path": path_erroneo,      # Esto limpia el error de "2 were given"
        "titulo": "Página no encontrada"
    }
    return render_view('error/404.html', context)