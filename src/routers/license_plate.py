from fastapi import APIRouter, UploadFile, File, Depends, Request
import numpy as np
import cv2

from dependencies import verify_api_key, get_license_plate_detector, get_ocr
from dtos import LicensePlateResponse
from services import ILicensePlateDetector, IOCR
from errors import LicensePlateErrors
from validators import validate_single_image

router = APIRouter()


@router.post(
    "/read-license-plate",
    response_model=LicensePlateResponse,
    dependencies=[Depends(verify_api_key)],
)
async def read_license_plate(
    request: Request,
    image: UploadFile = File(...),
    lp_detector: ILicensePlateDetector = Depends(get_license_plate_detector),
    ocr: IOCR = Depends(get_ocr),
):
    form = await request.form()

    validate_single_image(form)

    contents = await image.read()
    np_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if img is None:
        raise LicensePlateErrors.invalid_image()

    license_plate_crop = lp_detector.get_license_plate_image(img)
    license_plate_text = ocr.get_license_plate_text(license_plate_crop)

    return LicensePlateResponse(license_plate=license_plate_text)
