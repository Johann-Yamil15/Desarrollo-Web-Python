from urllib.parse import parse_qs

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ.get("REQUEST_METHOD", "GET")
        self.path = environ.get("PATH_INFO", "/")
        self.headers = self._parse_headers()
        self._form = None

    def _parse_headers(self):
        headers = {}
        for key, value in self.environ.items():
            if key.startswith("HTTP_"):
                headers[key[5:].replace("_", "-").title()] = value
        return headers

    def form(self):
        if self.method != "POST":
            return {}

        if self._form is not None:
            return self._form

        try:
            content_length = int(self.environ.get("CONTENT_LENGTH", 0))
        except (ValueError, TypeError):
            content_length = 0

        body = self.environ["wsgi.input"].read(content_length).decode("utf-8")

        parsed = parse_qs(body)

        # Convierte {'email': ['a@b.com']} → {'email': 'a@b.com'}
        self._form = {k: v[0] for k, v in parsed.items()}

        return self._form
