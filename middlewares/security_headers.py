def build_csp(env="prod"):
    """
    Construye la Content Security Policy de forma declarativa y escalable.
    Cambia permisos fácilmente según entorno (dev / prod).
    """

    csp = {
        "default-src": ["'self'"],

        "script-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://js.hcaptcha.com",
            "https://hcaptcha.com",
        ],

        "style-src": [
            "'self'",
            "'unsafe-inline'",  # Necesario para Bootstrap
            "https://cdn.jsdelivr.net",
        ],

        "img-src": [
            "'self'",
            "data:",
            "https://hcaptcha.com",
            "https://*.hcaptcha.com",
        ],

        "font-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
        ],

        "frame-src": [
            "https://hcaptcha.com",
            "https://*.hcaptcha.com",
        ],
        
        "connect-src": [
        "'self'",
        "https://cdn.jsdelivr.net",
    ],
    }

    # 🔧 Ajustes por entorno
    if env == "dev":
        csp["script-src"].append("'unsafe-eval'")

    # Construcción final del header
    return "; ".join(
        f"{directive} {' '.join(values)}"
        for directive, values in csp.items()
        if values
    )


def security_headers(headers, env="prod"):
    """
    Agrega headers de seguridad HTTP estándar + CSP.
    """

    headers.extend([
        ("X-Content-Type-Options", "nosniff"),
        ("X-Frame-Options", "SAMEORIGIN"),
        ("X-XSS-Protection", "1; mode=block"),
        ("Referrer-Policy", "strict-origin-when-cross-origin"),
        ("Content-Security-Policy", build_csp(env)),
    ])
