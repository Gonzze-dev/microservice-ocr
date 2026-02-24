import pytest
from unittest.mock import MagicMock

from errors.exceptions import ProblemDetailException
from validators.license_plate import validate_platform_code, validate_single_image


class TestValidatePlatformCode:
    def test_raises_when_platform_code_is_empty(self):
        with pytest.raises(ProblemDetailException) as exc_info:
            validate_platform_code("")
        assert exc_info.value.status == 400

    def test_raises_when_platform_code_is_none(self):
        with pytest.raises(ProblemDetailException) as exc_info:
            validate_platform_code(None)
        assert exc_info.value.status == 400

    def test_does_not_raise_when_platform_code_is_valid(self):
        validate_platform_code("PLATFORM_01")


class TestValidateSingleImage:
    def _make_form(self, file_count: int):
        items = []
        for i in range(file_count):
            upload = MagicMock()
            upload.filename = f"image_{i}.jpg"
            items.append(("image", upload))

        items.append(("platform_code", "PLATFORM_01"))

        form = MagicMock()
        form.multi_items.return_value = items
        return form

    def test_does_not_raise_when_single_image(self):
        form = self._make_form(file_count=1)
        validate_single_image(form)

    def test_raises_when_multiple_images(self):
        form = self._make_form(file_count=2)
        with pytest.raises(ProblemDetailException) as exc_info:
            validate_single_image(form)
        assert exc_info.value.status == 400
        assert exc_info.value.title == "Multiple Images"

    def test_does_not_raise_when_no_files(self):
        form = self._make_form(file_count=0)
        validate_single_image(form)
