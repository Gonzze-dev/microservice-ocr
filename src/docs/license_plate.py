from docs.problem_details import problem_response
from errors import AuthErrors, LicensePlateErrors, LPDetectorErrors, OCRErrors

_INSTANCE = "http://localhost:8000/read-license-plate"

# Declaring the 422 by hand stops FastAPI from adding its validation 422,
# so the HTTPValidationError schema is documented here.
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
    "The image could not be processed (`application/problem+json`), "
    "or the `image` field is missing (`application/json`, FastAPI validation format).",
    _INSTANCE,
    LPDetectorErrors.no_plate_detected(),
    LPDetectorErrors.low_confidence(0.61),
    OCRErrors.image_is_none(),
    OCRErrors.text_extraction_failed(),
)
_unprocessable["content"].update(_VALIDATION_ERROR_CONTENT)

READ_LICENSE_PLATE_RESPONSES = {
    200: {
        "description": "License plate read successfully.",
        "content": {"application/json": {"example": {"license_plate": "AB123CD"}}},
    },
    400: problem_response(
        "The image is not valid or several files were sent.",
        _INSTANCE,
        LicensePlateErrors.invalid_image(),
        LicensePlateErrors.multiple_images(),
    ),
    401: problem_response(
        "The `x-api-key` header is missing or the API key is invalid.",
        _INSTANCE,
        AuthErrors.invalid_api_key(),
    ),
    422: _unprocessable,
}
