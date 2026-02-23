from errors.exceptions import ProblemDetailException


class LicensePlateErrors:
    @staticmethod
    def invalid_image() -> ProblemDetailException:
        return ProblemDetailException(
            status=400,
            title="Invalid Image",
            detail="The uploaded file could not be decoded as a valid image.",
        )
