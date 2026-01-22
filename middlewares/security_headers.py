def security_headers(headers):
    headers.extend([
        ("X-Content-Type-Options", "nosniff"),
        ("X-Frame-Options", "SAMEORIGIN"),
        ("X-XSS-Protection", "1; mode=block"),
        ("Referrer-Policy", "no-referrer"),
        (
            "Content-Security-Policy",
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net https://js.hcaptcha.com https://hcaptcha.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://hcaptcha.com https://*.hcaptcha.com; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "frame-src https://hcaptcha.com https://*.hcaptcha.com;"
        )
    ])
