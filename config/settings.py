import os

# DB_CONN = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=DESKTOP-9OOGAMB;"
#     "DATABASE=DesarrolloWeb;"
#     "UID=sa;"
#     "PWD=123456789;"
#     "TrustServerCertificate=yes;"
# )
DB_CONN = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DesarrolloWeb.mssql.somee.com;"
    "DATABASE=DesarrolloWeb;"
    "UID=Johann_SQLLogin_1;"
    "PWD=3xwx5y8jq3;"
    "TrustServerCertificate=yes;"
)

def load_settings():
    if not DB_CONN:
        raise RuntimeError("Cadena de conexión no definida")
