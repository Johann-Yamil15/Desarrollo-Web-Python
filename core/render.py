import os

def render_view(template_name, context={}):
    # 1. Definimos la base en 'views' (sin el /home)
    base_path = os.path.join(os.getcwd(), 'views')
    
    # 2. El layout suele estar en la raíz de views o en una carpeta común
    # Ajustamos la ruta según donde tengas tu layout.html
    layout_path = os.path.join(base_path, 'home', 'layout.html')
    
    # Si moviste el layout a views/home, usa: os.path.join(base_path, 'home', 'layout.html')
    with open(layout_path, 'r', encoding='utf-8') as f:
        layout = f.read()
        
    # 3. Leer la vista específica (ej: 'home/index.html' o 'error/404.html')
    with open(os.path.join(base_path, template_name), 'r', encoding='utf-8') as f:
        content = f.read()
    
    final_html = layout.replace('{{content}}', content)

    # 4. Lógica de breadcrumbs (Mantenemos tu código intacto)
    if 'breadcrumbs' in context:
        bc_html = ""
        for i, bc in enumerate(context['breadcrumbs']):
            is_last = i == len(context['breadcrumbs']) - 1
            if is_last:
                bc_html += f'<span class="bc-current">{bc["name"]}</span>'
            else:
                bc_html += f'<a href="{bc["url"]}" class="bc-item">{bc["name"]}</a>'
                bc_html += '<span class="bc-sep">/</span>'
        
        final_html = final_html.replace('{{breadcrumbs_placeholder}}', bc_html)
    
    # 5. Reemplazo de variables del diccionario
    for key, value in context.items():
        placeholder = '{{' + key + '}}'
        final_html = final_html.replace(placeholder, str(value))
        
    return final_html.encode('utf-8')