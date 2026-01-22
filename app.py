from core.request import Request
from core.router import resolve
from core.response import Response
from core.static import serve_static
from middlewares.security_headers import security_headers
from config.database import load_settings

load_settings()


def application(environ, start_response):
    # =============================
    # 1. Archivos estáticos
    # =============================
    static_response = serve_static(environ)
    if static_response:
        status, body, headers = static_response
        security_headers(headers)
        start_response(status, headers)
        return [body]

    # =============================
    # 2. Request
    # =============================
    request = Request(environ)

    try:
        controller = resolve(request)

        # =============================
        # 3. Ruta encontrada
        # =============================
        if controller:
            result = controller(request)

            # Controller ya devuelve Response
            if isinstance(result, Response):
                response = result

            # Controller devuelve HTML (str)
            elif isinstance(result, str):
                response = Response(
                    result,
                    "200 OK",
                    [("Content-Type", "text/html; charset=utf-8")]
                )

            # Controller devuelve bytes
            elif isinstance(result, bytes):
                response = Response(
                    result,
                    "200 OK",
                    [("Content-Type", "application/octet-stream")]
                )

            else:
                raise TypeError(
                    f"Controller retornó tipo no soportado: {type(result)}"
                )

        # =============================
        # 4. Ruta NO encontrada
        # =============================
        else:
            response = Response(
                "",
                "302 Found",
                [("Location", "/404")]
            )

    # =============================
    # 5. Error interno REAL (500)
    # =============================
    except Exception as e:
        print("ERROR INTERNO:", e)

        response = Response(
            "<h1>500 - Error interno del servidor</h1>",
            "500 Internal Server Error",
            [("Content-Type", "text/html; charset=utf-8")]
        )

    # =============================
    # 6. Headers + respuesta final
    # =============================
    security_headers(response.headers)
    start_response(response.status, response.headers)
    return [response.body]
