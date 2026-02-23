from open_image_models import LicensePlateDetector as LPDetectorModel
from numpy import ndarray

from services.interfaces import ILicensePlateDetector
from errors import LPDetectorErrors


class LicensePlateDetector(ILicensePlateDetector):
    CONFIDENCE_THRESHOLD = 0.83

    def __init__(self):
        self._detector = LPDetectorModel(detection_model="yolo-v9-t-384-license-plate-end2end")

    def _detect_license_plate(self, image):
        if image is None:
            return None
        return self._detector.predict(image)

    def _crop_license_plate(self, image, bounding_box):
        x1, y1, x2, y2 = map(int, bounding_box)
        h, w, _ = image.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        return image[y1:y2, x1:x2]

    def get_license_plate_image(self, image) -> ndarray:
        detections = self._detect_license_plate(image)

        if not detections:
            raise LPDetectorErrors.no_plate_detected()

        license_plate_info = detections[0]
        confidence = license_plate_info.confidence

        if confidence < self.CONFIDENCE_THRESHOLD:
            raise LPDetectorErrors.low_confidence(confidence)

        bounding_box = license_plate_info.bounding_box
        return self._crop_license_plate(image, bounding_box)
