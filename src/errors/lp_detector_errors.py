from errors.exceptions import ProblemDetailException


class LPDetectorErrors:
    @staticmethod
    def no_plate_detected() -> ProblemDetailException:
        return ProblemDetailException(
            status=422,
            title="License Plate Detection Failed",
            detail="No license plate was detected in the image.",
        )

    @staticmethod
    def low_confidence(confidence: float) -> ProblemDetailException:
        return ProblemDetailException(
            status=422,
            title="Low Detection Confidence",
            detail=f"Confidence threshold not met: {confidence}",
        )
