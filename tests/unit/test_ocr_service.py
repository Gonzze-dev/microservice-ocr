import pytest
from unittest.mock import patch, MagicMock

from errors.exceptions import ProblemDetailException
from services.ocr import OCR


@pytest.fixture
def ocr_service():
    with patch.object(OCR, "__init__", lambda self: None):
        service = OCR.__new__(OCR)
        service._model = MagicMock()
        return service


class TestCleanText:
    def test_removes_special_characters(self, ocr_service):
        assert ocr_service._clean_text("AB-123.CD") == "AB123CD"

    def test_removes_spaces(self, ocr_service):
        assert ocr_service._clean_text("AB 123 CD") == "AB123CD"

    def test_keeps_alphanumeric(self, ocr_service):
        assert ocr_service._clean_text("ABC123") == "ABC123"

    def test_empty_string(self, ocr_service):
        assert ocr_service._clean_text("") == ""

    def test_only_special_characters(self, ocr_service):
        assert ocr_service._clean_text("---...") == ""


class TestExtractPlateText:
    def test_returns_none_when_result_is_none(self, ocr_service):
        assert ocr_service._extract_plate_text(None) is None

    def test_returns_none_when_result_is_empty(self, ocr_service):
        assert ocr_service._extract_plate_text([]) is None

    def test_filters_republica_argentina(self, ocr_service):
        ocr_result = [{"rec_texts": ["REPUBLICA ARGENTINA", "ABC123"]}]
        result = ocr_service._extract_plate_text(ocr_result)
        assert result == "ABC123"

    def test_filters_mercosur(self, ocr_service):
        ocr_result = [{"rec_texts": ["MERCOSUR", "AB123CD"]}]
        result = ocr_service._extract_plate_text(ocr_result)
        assert result == "AB123CD"

    def test_returns_valid_6_char_plate(self, ocr_service):
        ocr_result = [{"rec_texts": ["ABC123"]}]
        result = ocr_service._extract_plate_text(ocr_result)
        assert result == "ABC123"

    def test_returns_valid_7_char_plate(self, ocr_service):
        ocr_result = [{"rec_texts": ["AB123CD"]}]
        result = ocr_service._extract_plate_text(ocr_result)
        assert result == "AB123CD"

    def test_returns_none_when_text_too_short(self, ocr_service):
        ocr_result = [{"rec_texts": ["AB12"]}]
        assert ocr_service._extract_plate_text(ocr_result) is None

    def test_returns_none_when_text_too_long(self, ocr_service):
        ocr_result = [{"rec_texts": ["ABCD12345"]}]
        assert ocr_service._extract_plate_text(ocr_result) is None

    def test_returns_none_when_no_texts(self, ocr_service):
        ocr_result = [{"rec_texts": []}]
        assert ocr_service._extract_plate_text(ocr_result) is None

    def test_skips_ignored_and_returns_valid(self, ocr_service):
        ocr_result = [{"rec_texts": ["REPUBLICA", "ARGENTINA", "MERCOSUR", "AB123CD"]}]
        result = ocr_service._extract_plate_text(ocr_result)
        assert result == "AB123CD"


class TestGetLicensePlateText:
    def test_raises_when_image_is_none(self, ocr_service):
        with pytest.raises(ProblemDetailException) as exc_info:
            ocr_service.get_license_plate_text(None)
        assert exc_info.value.status == 422

    def test_raises_when_extraction_fails(self, ocr_service):
        ocr_service._model.predict.return_value = [{"rec_texts": []}]

        with pytest.raises(ProblemDetailException) as exc_info:
            ocr_service.get_license_plate_text(MagicMock())
        assert exc_info.value.status == 422
        assert exc_info.value.title == "Text Extraction Failed"

    def test_returns_cleaned_text_on_success(self, ocr_service):
        ocr_service._model.predict.return_value = [{"rec_texts": ["AB.123D"]}]

        result = ocr_service.get_license_plate_text(MagicMock())
        assert result == "AB123D"
