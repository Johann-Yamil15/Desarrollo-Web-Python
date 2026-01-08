def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")

    if path == "/":
        body = b"<h1>Hola mundo</h1>"
        status = "200 OK"
    else:
        body = b"<h1>404 - No encontrado</h1>"
        status = "404 Not Found"

    headers = [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(body)))
    ]

    start_response(status, headers)
    return [body]
