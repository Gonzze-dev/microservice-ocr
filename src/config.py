import os

API_KEY = os.getenv("API_KEY", "default-api-key-12345")

# Comma-separated origins. Empty = all are allowed.
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
] or ["*"]
