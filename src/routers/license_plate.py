from fastapi import APIRouter, UploadFile, File, Depends, Request
import numpy as np
import cv2

from dependencies import verify_api_key, get_license_plate_detector, get_ocr
from docs import READ_LICENSE_PLATE_RESPONSES
from dtos import LicensePlateResponse
from services import ILicensePlateDetector, IOCR
from errors import LicensePlateErrors
from validators import validate_single_image

router = APIRouter(tags=["License Plate"])


@router.post(
    "/read-license-plate",
    response_model=LicensePlateResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Read the license plate from an image",
    responses=READ_LICENSE_PLATE_RESPONSES,
)
async def read_license_plate(
    request: Request,
    image: UploadFile = File(
        ...,
        description="Vehicle image (JPG, PNG, etc.). Only one file per request is accepted.",
    ),
    lp_detector: ILicensePlateDetector = Depends(get_license_plate_detector),
    ocr: IOCR = Depends(get_ocr),
):
    """
    Receives **a single** vehicle image, detects the license plate region
    (detection confidence threshold: `0.83`) and returns the text read.
    Words unrelated to the plate (e.g. `REPUBLICA ARGENTINA`, `MERCOSUR`)
    are filtered out automatically.
    """
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
