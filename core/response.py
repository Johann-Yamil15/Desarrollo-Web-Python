class Response:
    def __init__(self, body="", status="200 OK", headers=None, content_type="text/html"):
        self.body = body.encode("utf-8")
        self.status = status

        self.headers = headers or []
        self.headers.append(("Content-Type", f"{content_type}; charset=utf-8"))
        self.headers.append(("Content-Length", str(len(self.body))))
