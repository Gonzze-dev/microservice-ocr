from fastapi import Header, Request

from config import API_KEY
from services import ILicensePlateDetector, IOCR
from errors import AuthErrors


async def verify_api_key(x_api_key: str = Header(...)):
    print(x_api_key)
    print(API_KEY)
    if x_api_key != API_KEY:
        raise AuthErrors.invalid_api_key()


def get_license_plate_detector(request: Request) -> ILicensePlateDetector:
    return request.app.state.license_plate_detector


def get_ocr(request: Request) -> IOCR:
    return request.app.state.ocr
