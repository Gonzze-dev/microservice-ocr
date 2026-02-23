from errors.exceptions import ProblemDetailException


class OCRErrors:
    @staticmethod
    def image_is_none() -> ProblemDetailException:
        return ProblemDetailException(
            status=422,
            title="OCR Processing Failed",
            detail="The provided image for OCR processing is null.",
        )

    @staticmethod
    def text_extraction_failed() -> ProblemDetailException:
        return ProblemDetailException(
            status=422,
            title="Text Extraction Failed",
            detail="Could not extract license plate text from the image.",
        )
