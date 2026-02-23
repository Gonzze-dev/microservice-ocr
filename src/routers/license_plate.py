from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
import numpy as np
import cv2

from dependencies import verify_api_key, get_license_plate_detector, get_ocr
from services import ILicensePlateDetector, IOCR
from errors import LicensePlateErrors

router = APIRouter()


@router.post("/read-license-plate", dependencies=[Depends(verify_api_key)])
async def read_license_plate(
    image: UploadFile = File(...),
    lp_detector: ILicensePlateDetector = Depends(get_license_plate_detector),
    ocr: IOCR = Depends(get_ocr),
):
    contents = await image.read()
    np_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if img is None:
        raise LicensePlateErrors.invalid_image()

    license_plate_crop = lp_detector.get_license_plate_image(img)
    license_plate_text = ocr.get_license_plate_text(license_plate_crop)

    return JSONResponse(content={"license_plate": license_plate_text})
