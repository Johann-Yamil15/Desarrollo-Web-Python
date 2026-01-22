import os
import uuid
from datetime import datetime
from config.database import get_connection

UPLOAD_DIR = "static/carrusel"
WEB_PATH = "/static/carrusel"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def carrusel(request):

    # =============================
    # GET
    # =============================
    if request.method == "GET":
        print("➡️ GET /carrusel")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ruta_relativa
            FROM Carrusel
            ORDER BY fecha_carga ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print(f"📦 Imágenes encontradas: {len(rows)}")

        items = ""
        for i, row in enumerate(rows):
            active = "active" if i == 0 else ""
            items += f"""
                <div class="carousel-item {active}">
                    <img src="{row[0]}" class="d-block w-100">
                </div>
            """

        html = open("views/carrusel.html", encoding="utf-8").read()
        return html.replace("{{items_carrusel}}", items)

    # =============================
    # POST
    # =============================
    try:
        print("➡️ POST /carrusel")

        file = request.files.get("imagen")

        if not file:
            return "<h3>Error: Imagen requerida</h3>"

        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            return "<h3>Error: Formato no permitido</h3>"

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        unique_name = f"{uuid.uuid4().hex}{ext}"
        real_path = os.path.join(UPLOAD_DIR, unique_name)
        web_path = f"{WEB_PATH}/{unique_name}"

        # 💾 Guardar archivo en disco
        file.save(real_path)

        # 💾 Guardar en BD (FIX CLAVE AQUÍ 👇)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Carrusel (nombre_archivo, ruta_relativa, fecha_carga)
            VALUES (%s, %s, %s)
        """, (
            unique_name,
            web_path,
            datetime.now()
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return """
            <h2>✔ Imagen agregada al carrusel</h2>
            <a href="/carrusel">Volver</a>
        """

    except Exception as e:
        print("🔥 ERROR:", e)
        return f"<pre>{e}</pre>"
