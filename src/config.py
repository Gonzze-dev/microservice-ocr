import os

API_KEY = os.getenv("API_KEY", "default-api-key-12345")

# Orígenes separados por coma. Vacío = se permiten todos.
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
] or ["*"]
