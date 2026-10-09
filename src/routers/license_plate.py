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
    summary="Leer la patente de una imagen",
    responses=READ_LICENSE_PLATE_RESPONSES,
)
async def read_license_plate(
    request: Request,
    image: UploadFile = File(
        ...,
        description="Imagen del vehículo (JPG, PNG, etc.). Solo se admite un archivo por request.",
    ),
    lp_detector: ILicensePlateDetector = Depends(get_license_plate_detector),
    ocr: IOCR = Depends(get_ocr),
):
    """
    Recibe **una única** imagen de un vehículo, detecta la región de la patente
    (umbral de confianza de detección: `0.83`) y devuelve el texto leído.
    Palabras ajenas a la patente (p. ej. `REPUBLICA ARGENTINA`, `MERCOSUR`)
    se filtran automáticamente.
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
