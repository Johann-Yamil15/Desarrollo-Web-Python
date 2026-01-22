from urllib.parse import parse_qs
import io
import re

class UploadedFile:
    def __init__(self, filename, content_type, file):
        self.filename = filename
        self.content_type = content_type
        self.file = file  # BytesIO

    def save(self, path):
        with open(path, "wb") as f:
            while True:
                chunk = self.file.read(8192)
                if not chunk:
                    break
                f.write(chunk)


class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ.get("REQUEST_METHOD", "GET")
        self.path = environ.get("PATH_INFO", "/")
        self.headers = self._parse_headers()

        self._form = {}
        self.files = {}

        if self.method == "POST":
            self._parse_body()

    def _parse_headers(self):
        headers = {}
        for key, value in self.environ.items():
            if key.startswith("HTTP_"):
                headers[key[5:].replace("_", "-").title()] = value
        return headers

    def _parse_body(self):
        content_type = self.environ.get("CONTENT_TYPE", "")

        try:
            length = int(self.environ.get("CONTENT_LENGTH", 0))
        except (ValueError, TypeError):
            length = 0

        body = self.environ["wsgi.input"].read(length)

        # -------------------------------
        # FORM NORMAL
        # -------------------------------
        if content_type.startswith("application/x-www-form-urlencoded"):
            parsed = parse_qs(body.decode())
            self._form = {k: v[0] for k, v in parsed.items()}
            return

        # -------------------------------
        # FORM + ARCHIVOS
        # -------------------------------
        if content_type.startswith("multipart/form-data"):
            boundary = content_type.split("boundary=")[-1].encode()
            parts = body.split(b"--" + boundary)

            for part in parts:
                if b"Content-Disposition" not in part:
                    continue

                headers, content = part.split(b"\r\n\r\n", 1)
                content = content.rstrip(b"\r\n--")

                header_text = headers.decode(errors="ignore")

                name_match = re.search(r'name="([^"]+)"', header_text)
                filename_match = re.search(r'filename="([^"]+)"', header_text)
                type_match = re.search(r"Content-Type: ([^\r\n]+)", header_text)

                if not name_match:
                    continue

                name = name_match.group(1)

                # 🟢 ARCHIVO
                if filename_match:
                    filename = filename_match.group(1)
                    ctype = type_match.group(1) if type_match else "application/octet-stream"

                    self.files[name] = UploadedFile(
                        filename=filename,
                        content_type=ctype,
                        file=io.BytesIO(content)
                    )

                # 🟡 CAMPO NORMAL
                else:
                    self._form[name] = content.decode().strip()

    def form(self):
        return self._form
