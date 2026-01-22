from controllers.home_controller import home
from controllers.auth_controller import login, register
from controllers.prueba_controller import prueba
from controllers.error_controller import error
from controllers.form_controller import form_test
from controllers.carousel_controller import carrusel


routes = {
    # Home
    ("GET", "/"): home, 
    ("POST", "/"): home, 
    # prueba
    ("GET", "/prueba"): prueba,
    ("POST", "/prueba"): prueba,
    # carrucel
    ("GET", "/carrusel"): carrusel,
    ("POST", "/carrusel"): carrusel,
    # Formulario de validaciones (SIN DB)
    ("GET", "/form-test"): form_test,
    ("POST", "/form-test"): form_test,
    # Error 404
    ("GET", "/404"): error,
    #Login
    ("GET", "/login"): login,
    ("POST", "/login"): login,
    #Register
    ("GET", "/register"): register,
    ("POST", "/register"): register,
}

def resolve(request):
    return routes.get((request.method, request.path))