from open_image_models import LicensePlateDetector as LPDetectorModel
from numpy import ndarray
import cv2

from services.interfaces import ILicensePlateDetector
from errors import LPDetectorErrors


class LicensePlateDetector(ILicensePlateDetector):
    CONFIDENCE_THRESHOLD = 0.70

    def __init__(self):
        self._detector = LPDetectorModel(detection_model="yolo-v9-t-384-license-plate-end2end")

    def _detect_license_plate(self, image):
        if image is None:
            return None
        return self._detector.predict(image)

    def _crop_license_plate(self, image, bounding_box, name_img="debug_cropped_license_plate.png"):
        x1, y1, x2, y2 = map(int, bounding_box)
        h, w, _ = image.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        return image[y1:y2, x1:x2]

    def debug_draw_bounding_box_points(
        self,
        image,
        detections,
        name_img="debug_bounding_boxes.png"
    ):
        """Provisorio: dibuja los puntos del bounding box. Rojo = X, Verde = Y."""
        img_copy = image.copy()
        radius = 8
        thickness = -1
        red = (0, 0, 255)
        green = (0, 255, 0)
        yellow = (0, 255, 255)
        blue = (0, 165, 255)

        for detection in detections:
            x1, y1, x2, y2 = map(int, tuple(detection.bounding_box))
            cv2.circle(img_copy, (x1, y1), radius, color=red, thickness=-1) # Rojo
            cv2.circle(img_copy, (x2, y1), radius, color=yellow, thickness=-1) # Amarillo
            cv2.circle(img_copy, (x1, y2), radius, color=green, thickness=-1) # Verde
            cv2.circle(img_copy, (x2, y2), radius, color=blue, thickness=-1) # Azul

        cv2.imwrite(name_img, img_copy)
        print(f"Imagen guardada en {name_img}")
        return img_copy

    def _select_largest_plate_by_axis_Y(self, detections):
        return max(
            detections,
            key=lambda d: abs(tuple(d.bounding_box)[1] - tuple(d.bounding_box)[3])
        )

    def get_license_plate_image(
        self, 
        image,
    ) -> ndarray:
        detections = self._detect_license_plate(image)

        if not detections:
            raise LPDetectorErrors.no_plate_detected()

        license_plate_info = self._select_largest_plate_by_axis_Y(detections)

        confidence = license_plate_info.confidence

        if confidence < self.CONFIDENCE_THRESHOLD:
            raise LPDetectorErrors.low_confidence(confidence)

        bounding_box = license_plate_info.bounding_box
        return self._crop_license_plate(image, bounding_box)
