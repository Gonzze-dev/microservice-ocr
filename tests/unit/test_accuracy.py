import os
import cv2
import pytest

from services.license_plate_detector import LicensePlateDetector
from services.ocr import OCR
from errors.exceptions import ProblemDetailException

IMGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "src", "imgs-v")

EXPECTED_PLATES = [
    ("image-1.jpg", "AA464PA"),
    ("image-2.jpg", "34NH9258"),
    ("image-3.jpg", "AA464ON"),
    ("image-4.jpg", "AA464PY"),
    ("image-5.jpg", "AG156OP"),
    ("image-6.jpg", "AG6OP"),
    ("image-7.jpg", "AG16OP"),
]


@pytest.fixture(scope="module")
def detector():
    return LicensePlateDetector()


@pytest.fixture(scope="module")
def ocr():
    return OCR()


@pytest.mark.slow
class TestAccuracy:
    def _read_plate(self, detector, ocr, image_path):
        img = cv2.imread(image_path)
        assert img is not None, f"Could not read image: {image_path}"

        try:
            crop = detector.get_license_plate_image(img)
            text = ocr.get_license_plate_text(crop)
            return text
        except ProblemDetailException as e:
            return f"ERROR: {e.title} - {e.detail}"

    def test_accuracy_report(self, detector, ocr):
        results = []
        passed = 0
        total = len(EXPECTED_PLATES)

        for filename, expected in EXPECTED_PLATES:
            path = os.path.join(IMGS_DIR, filename)
            result = self._read_plate(detector, ocr, path)
            match = result == expected
            if match:
                passed += 1
            results.append((filename, expected, result, match))

        report_lines = [
            "",
            "=" * 65,
            "LICENSE PLATE RECOGNITION - ACCURACY REPORT",
            "=" * 65,
        ]
        for filename, expected, result, match in results:
            status = "OK" if match else "FAIL"
            report_lines.append(
                f"  [{status:4s}] {filename:<12s}  expected={expected:<10s}  got={result}"
            )
        report_lines.append("-" * 65)
        report_lines.append(
            f"  Result: {passed}/{total} correct ({passed / total * 100:.1f}%)"
        )
        report_lines.append("=" * 65)

        print("\n".join(report_lines))

        failed = [r for r in results if not r[3]]
        if failed:
            fail_names = ", ".join(r[0] for r in failed)
            pytest.fail(
                f"{len(failed)}/{total} images failed: {fail_names} "
                f"({passed / total * 100:.1f}% accuracy)"
            )
