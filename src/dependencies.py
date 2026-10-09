from fastapi import Request, Security
from fastapi.security import APIKeyHeader

from config import API_KEY
from services import ILicensePlateDetector, IOCR
from errors import AuthErrors

api_key_header = APIKeyHeader(
    name="x-api-key",
    scheme_name="ApiKeyAuth",
    description="API key configurada en la variable de entorno `API_KEY`.",
    auto_error=False,
)


async def verify_api_key(x_api_key: str | None = Security(api_key_header)):
    if x_api_key != API_KEY:
        raise AuthErrors.invalid_api_key()


def get_license_plate_detector(request: Request) -> ILicensePlateDetector:
    return request.app.state.license_plate_detector


def get_ocr(request: Request) -> IOCR:
    return request.app.state.ocr
