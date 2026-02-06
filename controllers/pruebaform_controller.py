from utils.validators import validate_form
from datetime import date
# Importa esto para procesar los datos del formulario POST
import urllib.parse 

def form_test(env): # Cambiamos el nombre de 'request' a 'env' para ser claros
    # --- CONFIGURACIÓN PARA EXTRAER DATOS DEL DICCIONARIO 'env' ---
    method = env.get('REQUEST_METHOD', 'GET')
    
    # Función interna para simular request.form()
    def get_form_data():
        try:
            request_body_size = int(env.get('CONTENT_LENGTH', 0))
            request_body = env['wsgi.input'].read(request_body_size).decode('utf-8')
            # Convierte la cadena 'name=Juan&email=test@test.com' en un diccionario
            parsed_data = urllib.parse.parse_qs(request_body)
            # parse_qs devuelve listas, las convertimos a valores simples
            return {k: v[0] for k, v in parsed_data.items()}
        except:
            return {}

    # 1. Intentar cargar el archivo HTML del formulario
    try:
        with open("views/prueba/form_test.html", encoding="utf-8") as f:
            content_html = f.read()
    except FileNotFoundError:
        return "Error: No se encontró el archivo 'views/prueba/form_test.html'."

    # 2. Intentar cargar el Layout Principal
    try:
        with open("views/home/layout.html", encoding="utf-8") as f:
            layout_html = f.read()
    except FileNotFoundError:
        return "Error: No se encontró el archivo de layout principal."

    fields = ["name", "username", "email", "phone", "birthdate"]
    data = {f: "" for f in fields}
    errors = {}
    today_str = date.today().isoformat()

    # 3. Procesar el POST usando nuestras nuevas variables
    if method == "POST":
        data = get_form_data() # Obtenemos los datos del body
        errors = validate_form(data)

        if not errors:
            success_msg = f"""
            <div class="container mt-5 text-center">
                <div class="carousel-card p-5 shadow">
                    <div class="icon-circle bg-success text-white mb-4" style="width:80px; height:80px; font-size:40px; margin:0 auto; display:flex; align-items:center; justify-content:center; border-radius:50%;">
                        <i class="fas fa-check"></i>
                    </div>
                    <h2 class="fw-bold text-dark">¡Validación Exitosa!</h2>
                    <p class="text-muted">Los datos de <b>{data.get('name', '')}</b> son correctos.</p>
                    <a href="/pruebaform" class="btn btn-primary mt-3 px-5" style="border-radius:12px; background:var(--render-blue);">
                        Volver a intentar
                    </a>
                </div>
            </div>
            """
            return layout_html.replace("{{content}}", success_msg).replace("{{titulo}}", "Éxito")

    # 4. Reemplazar placeholders (Igual que antes pero usando 'data')
    for field in fields:
        content_html = content_html.replace(f"{{{{{field}}}}}", str(data.get(field, "")))
        
        if field in errors:
            content_html = content_html.replace(f"{{{{error_{field}}}}}", errors[field])
            content_html = content_html.replace(f"{{{{class_{field}}}}}", "error-input")
        else:
            content_html = content_html.replace(f"{{{{error_{field}}}}}", "")
            content_html = content_html.replace(f"{{{{class_{field}}}}}", "")

    content_html = content_html.replace("{{checked_terms}}", "checked" if "terms" in data else "")
    content_html = content_html.replace("{{error_terms}}", errors.get("terms", ""))
    content_html = content_html.replace("{{today}}", today_str)

    # 5. Ensamblaje Final
    final_output = layout_html.replace("{{content}}", content_html)
    final_output = final_output.replace("{{titulo}}", "Prueba de Validación")
    final_output = final_output.replace("{{breadcrumbs_placeholder}}", "My Project / Prueba Error")

    return final_output