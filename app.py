from core.request import Request
from core.router import resolve
from core.response import Response
from core.static import serve_static
from middlewares.security_headers import security_headers
from config.database import load_settings


load_settings()

def application(environ, start_response):
    # =============================
    # Archivos estáticos
    # =============================
    static_response = serve_static(environ)
    if static_response:
        status, body, headers = static_response
        start_response(status, headers)
        return [body]

    request = Request(environ)

    try:
        controller = resolve(request)

        # =============================
        # Ruta encontrada
        # =============================
        if controller:
            body = controller(request)
            response = Response(body)

        # =============================
        # Ruta NO encontrada → /404
        # =============================
        else:
            response = Response(
                "",
                "302 Found",
                [("Location", "/404")]
            )

    # =============================
    # Error interno → /404
    # =============================
    except Exception as e:
        print("ERROR:", e)  # log básico
        response = Response(
            "",
            "302 Found",
            [("Location", "/404")]
        )

    security_headers(response.headers)
    start_response(response.status, response.headers)
    return [response.body]
