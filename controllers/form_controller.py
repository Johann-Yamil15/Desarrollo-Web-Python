from utils.validators import validate_form

def form_test(request):
    try:
        with open("views/form_test.html", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        return "Error: No se encontró el archivo HTML."

    # Valores iniciales
    fields = ["name", "username", "age", "email", "phone", "birthdate"]
    data = {f: "" for f in fields}
    errors = {}

    if request.method == "POST":
        data = request.form()
        errors = validate_form(data)

        if not errors:
            return """
            <div style="text-align:center; font-family:sans-serif; margin-top:50px;">
                <h2 style="color:green;">✔ ¡Datos Válidos!</h2>
                <p>El formulario pasó todas las pruebas.</p>
                <a href="/form-test" style="text-decoration:none; color:blue;">Volver a probar</a>
            </div>
            """

    # Reemplazar valores y estados de error
    for field in fields:
        # Rellenar el valor que el usuario ya escribió
        html = html.replace(f"{{{{{field}}}}}", data.get(field, ""))
        
        # Si hay error, poner el mensaje y la clase CSS 'error-input'
        if field in errors:
            html = html.replace(f"{{{{error_{field}}}}}", errors[field])
            html = html.replace(f"{{{{class_{field}}}}}", "error-input")
        else:
            html = html.replace(f"{{{{error_{field}}}}}", "")
            html = html.replace(f"{{{{class_{field}}}}}", "")

    # Caso especial: Checkbox
    if "terms" in data:
        html = html.replace("{{checked_terms}}", "checked")
    else:
        html = html.replace("{{checked_terms}}", "")
    
    html = html.replace("{{error_terms}}", errors.get("terms", ""))

    return html