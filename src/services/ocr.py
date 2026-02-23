from paddleocr import PaddleOCR
from re import sub

from services.interfaces import IOCR
from errors import OCRErrors


class OCR(IOCR):
    IGNORED_WORDS = [
        "REPUBLICA",
        "ARGENTINA",
        "MERCOSUR",
        "BRASIL",
        "URUGUAY",
    ]

    def __init__(self):
        self._model = PaddleOCR(
            use_textline_orientation=True,
            lang="es",
            enable_mkldnn=False,
        )

    def _clean_text(self, text: str) -> str:
        return sub(r'[^a-zA-Z0-9]', '', text)

    def _extract_plate_text(self, ocr_result) -> str | None:
        """
        Processes PaddleOCR output and extracts the license plate text,
        filtering out headers like 'República Argentina'.
        """
        if not ocr_result or len(ocr_result) == 0:
            return None

        data = ocr_result[0]
        texts = data.get('rec_texts', [])

        for text in texts:
            current_text = text.upper()
            text_for_check = current_text.replace(" ", "").replace(".", "")

            if any(ignored in text_for_check for ignored in self.IGNORED_WORDS):
                continue

            if 6 <= len(text_for_check) <= 7:
                return current_text

        return None

    def get_license_plate_text(self, image) -> str:
        if image is None:
            raise OCRErrors.image_is_none()

        result = self._model.predict(image)

        extracted_text = self._extract_plate_text(result)
        if extracted_text is None:
            raise OCRErrors.text_extraction_failed()

        return self._clean_text(extracted_text)
