from controllers.home_controller import home
from controllers.auth_controller import login, register
from controllers.prueba_controller import prueba
from controllers.error_controller import error
routes = {
    # Home
    ("GET", "/"): home, 
    ("POST", "/"): home, 
    # prueba
    ("GET", "/prueba"): prueba,
    ("POST", "/prueba"): prueba,
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