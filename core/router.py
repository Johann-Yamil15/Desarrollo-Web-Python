from controllers.home_controller import index_action
from controllers.user_controller import user_manager_action, user_api_dispatcher
from controllers.carrusel_controller import carrusel_controller  # <--- IMPORTANTE
from controllers.error_controller import not_found_action
from controllers.pruebaform_controller import form_test

def get_route_handler(path, method):
    # Diccionario de rutas: (path, method) -> function
    routes = {
        ('/', 'GET'): lambda bc, env: index_action(bc),
        ('/users', 'GET'): lambda bc, env: user_manager_action(bc),

        # Estos sí usan ambos
        ('/carrusel', 'GET'): lambda bc, env: carrusel_controller(bc, env),
        ('/carrusel', 'POST'): lambda bc, env: carrusel_controller(bc, env),

        # Prueba de formulario
        ('/pruebaform', 'GET'): lambda bc, env: form_test(env),
        ('/pruebaform', 'POST'): lambda bc, env: form_test(env),

        # La API se centraliza en el dispatcher
        ('/api/users', 'GET'): lambda bc, env: user_api_dispatcher(env, 'GET'),
        ('/api/users', 'POST'): lambda bc, env: user_api_dispatcher(env, 'POST'),
        ('/api/users', 'PUT'): lambda bc, env: user_api_dispatcher(env, 'PUT'),
        ('/api/users', 'DELETE'): lambda bc, env: user_api_dispatcher(env, 'DELETE'),
    }

    handler = routes.get((path, method))

    if handler:
        return handler, '200 OK'

    # Si no existe, devolvemos el controlador 404
    return not_found_action, '404 Not Found'
