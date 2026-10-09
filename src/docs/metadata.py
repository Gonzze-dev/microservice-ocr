API_VERSION = "1.0.0"

API_DESCRIPTION = """
Microservicio que detecta la patente de un vehículo en una imagen (YOLOv9)
y extrae su texto alfanumérico (PaddleOCR).

Los errores de negocio siguen el estándar
[RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457)
(`application/problem+json`). Los errores de validación de request
(campo faltante) los genera FastAPI con su formato propio.
"""

# URL relativa: Swagger UI usa el host desde el que se sirve la documentación.
SERVERS = [{"url": "/", "description": "Servidor actual"}]

LICENSE_INFO = {"name": "MIT", "identifier": "MIT"}

OPENAPI_TAGS = [
    {"name": "Health", "description": "Estado del servicio"},
    {"name": "License Plate", "description": "Lectura de patentes"},
]
