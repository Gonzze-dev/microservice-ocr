import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from errors.exceptions import ProblemDetailException
from services.license_plate_detector import LicensePlateDetector


@pytest.fixture
def detector():
    with patch.object(LicensePlateDetector, "__init__", lambda self: None):
        service = LicensePlateDetector.__new__(LicensePlateDetector)
        service._detector = MagicMock()
        return service


def _make_detection(confidence: float, bounding_box: tuple = (10, 10, 100, 50)):
    detection = MagicMock()
    detection.confidence = confidence
    detection.bounding_box = bounding_box
    return detection


class TestGetLicensePlateImage:
    def test_raises_when_no_plate_detected(self, detector):
        detector._detector.predict.return_value = []

        with pytest.raises(ProblemDetailException) as exc_info:
            detector.get_license_plate_image(np.zeros((100, 200, 3), dtype=np.uint8))
        assert exc_info.value.status == 422
        assert exc_info.value.title == "License Plate Detection Failed"

    def test_raises_when_detection_returns_none(self, detector):
        detector._detector.predict.return_value = None

        with pytest.raises(ProblemDetailException) as exc_info:
            detector.get_license_plate_image(np.zeros((100, 200, 3), dtype=np.uint8))
        assert exc_info.value.status == 422

    def test_raises_when_confidence_below_threshold(self, detector):
        detection = _make_detection(confidence=0.50)
        detector._detector.predict.return_value = [detection]

        with pytest.raises(ProblemDetailException) as exc_info:
            detector.get_license_plate_image(np.zeros((100, 200, 3), dtype=np.uint8))
        assert exc_info.value.status == 422
        assert exc_info.value.title == "Low Detection Confidence"

    def test_raises_when_confidence_just_below_threshold(self, detector):
        detection = _make_detection(confidence=0.82)
        detector._detector.predict.return_value = [detection]

        with pytest.raises(ProblemDetailException) as exc_info:
            detector.get_license_plate_image(np.zeros((100, 200, 3), dtype=np.uint8))
        assert exc_info.value.status == 422

    def test_returns_cropped_image_on_success(self, detector):
        image = np.ones((100, 200, 3), dtype=np.uint8) * 255
        detection = _make_detection(confidence=0.95, bounding_box=(10, 20, 50, 40))
        detector._detector.predict.return_value = [detection]

        result = detector.get_license_plate_image(image)

        assert result.shape == (20, 40, 3)  # y2-y1=20, x2-x1=40
        assert np.all(result == 255)

    def test_returns_image_when_confidence_at_threshold(self, detector):
        image = np.ones((100, 200, 3), dtype=np.uint8)
        detection = _make_detection(confidence=0.83, bounding_box=(0, 0, 50, 50))
        detector._detector.predict.return_value = [detection]

        result = detector.get_license_plate_image(image)
        assert result.shape == (50, 50, 3)


class TestCropLicensePlate:
    def test_crops_correctly(self, detector):
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        image[10:50, 20:80] = 128

        crop = detector._crop_license_plate(image, (20, 10, 80, 50))

        assert crop.shape == (40, 60, 3)
        assert np.all(crop == 128)

    def test_clamps_negative_coordinates(self, detector):
        image = np.zeros((100, 200, 3), dtype=np.uint8)

        crop = detector._crop_license_plate(image, (-10, -5, 50, 30))

        assert crop.shape == (30, 50, 3)

    def test_clamps_coordinates_exceeding_image_bounds(self, detector):
        image = np.zeros((100, 200, 3), dtype=np.uint8)

        crop = detector._crop_license_plate(image, (150, 80, 300, 150))

        assert crop.shape == (20, 50, 3)  # clamped to (150,80,200,100)
