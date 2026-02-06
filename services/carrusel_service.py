import os
import uuid
from datetime import datetime
from config.database import get_connection
from models.carrusel_model import CarruselItem

UPLOAD_DIR = "static/Images/Carrusel"
WEB_PATH = "/static/Images/Carrusel"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

class CarruselService:
    @staticmethod
    def get_all_items():
        conn = get_connection()
        cursor = conn.cursor(as_dict=True)
        try:
            cursor.execute("SELECT * FROM Carrusel ORDER BY fecha_carga ASC")
            return [CarruselItem.from_dict(row).to_dict() for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def save_image(file):
        if not file: return False, "No hay archivo"
        
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, "Formato no permitido"

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        unique_name = f"{uuid.uuid4().hex}{ext}"
        real_path = os.path.join(UPLOAD_DIR, unique_name)
        web_path = f"{WEB_PATH}/{unique_name}"

        # Guardar en disco
        file.save(real_path)

        # Guardar en BD
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Carrusel (nombre_archivo, ruta_relativa, fecha_carga)
                VALUES (%s, %s, GETDATE())
            """, (unique_name, web_path))
            conn.commit()
            return True, "Imagen guardada"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()