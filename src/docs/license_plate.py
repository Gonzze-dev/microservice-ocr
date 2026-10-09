from docs.problem_details import problem_response
from errors import AuthErrors, LicensePlateErrors, LPDetectorErrors, OCRErrors

_INSTANCE = "http://localhost:8000/read-license-plate"

# Declarar el 422 a mano evita que FastAPI agregue su 422 de validación,
# así que el esquema de HTTPValidationError se documenta acá.
_VALIDATION_ERROR_CONTENT = {
    "application/json": {
        "schema": {
            "title": "HTTPValidationError",
            "type": "object",
            "properties": {
                "detail": {
                    "type": "array",
                    "items": {
                        "title": "ValidationError",
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "properties": {
                            "loc": {
                                "type": "array",
                                "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                            },
                            "msg": {"type": "string"},
                            "type": {"type": "string"},
                            "input": {},
                        },
                    },
                }
            },
        },
        "example": {
            "detail": [
                {"type": "missing", "loc": ["body", "image"], "msg": "Field required", "input": None}
            ]
        },
    }
}

_unprocessable = problem_response(
    "No se pudo procesar la imagen (`application/problem+json`), "
    "o falta el campo `image` (`application/json`, formato de validación de FastAPI).",
    _INSTANCE,
    LPDetectorErrors.no_plate_detected(),
    LPDetectorErrors.low_confidence(0.61),
    OCRErrors.image_is_none(),
    OCRErrors.text_extraction_failed(),
)
_unprocessable["content"].update(_VALIDATION_ERROR_CONTENT)

READ_LICENSE_PLATE_RESPONSES = {
    200: {
        "description": "Patente leída correctamente.",
        "content": {"application/json": {"example": {"license_plate": "AB123CD"}}},
    },
    400: problem_response(
        "La imagen no es válida o se enviaron varios archivos.",
        _INSTANCE,
        LicensePlateErrors.invalid_image(),
        LicensePlateErrors.multiple_images(),
    ),
    401: problem_response(
        "Falta el header `x-api-key` o la API key es inválida.",
        _INSTANCE,
        AuthErrors.invalid_api_key(),
    ),
    422: _unprocessable,
}
