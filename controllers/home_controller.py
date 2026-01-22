from config.database import test_connection

def home(request):
    mensaje = "<h1>Hola mundo</h1>"

    try:
        fecha = test_connection()
        mensaje += f"<p>SQL Server conectado: {fecha}</p>"
    except Exception as e:
        mensaje += f"<p style='color:red'>{e}</p>"

# Botón para ir a /prueba
    mensaje += """
        <br><br>
        <a href="/prueba">
            <button style="padding:10px 15px;font-size:16px;cursor:pointer;">
                Ir a Prueba (hCaptcha)
            </button>
        </a>
    """
    # Botón prueva eror de ruta y redireccion a /404
    mensaje += """
        <br><br>
        <a href="/ruta-inexistente">
            <button style="padding:10px 15px;font-size:16px;cursor:pointer;">
                simulacion de ruta corumpta (404)
            </button>
        </a>
    """
    # Botón para ir a /form-test
    mensaje += """
        <br><br>
        <a href="/form-test">
            <button style="padding:10px 15px;font-size:16px;cursor:pointer;">
                test de formulario (validaciones)
            </button>
        </a>
    """
    # Botón para ir a /carrusel
    mensaje += """
        <br><br>
        <a href="/carrusel">
            <button style="padding:10px 15px;font-size:16px;cursor:pointer;">
                carrusel
            </button>
            </button>
        </a>
    """
    return mensaje
