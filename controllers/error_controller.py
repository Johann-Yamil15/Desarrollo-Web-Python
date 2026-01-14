from config.database import get_connection
from services.user_service import hash_password
from core.response import Response
from datetime import datetime

# Registration controller
def error(request):
    if request.method == "GET":
        return open("views/Error/404.html", encoding="utf-8").read()