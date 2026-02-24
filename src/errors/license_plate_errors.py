from errors.exceptions import ProblemDetailException


class LicensePlateErrors:
    @staticmethod
    def platform_code_is_required() -> ProblemDetailException:
        return ProblemDetailException(
            status=400,
            title="Platform Code Required",
            detail="The platform code is required and cannot be empty.",
        )

    @staticmethod
    def invalid_image() -> ProblemDetailException:
        return ProblemDetailException(
            status=400,
            title="Invalid Image",
            detail="The uploaded file could not be decoded as a valid image.",
        )

    @staticmethod
    def multiple_images() -> ProblemDetailException:
        return ProblemDetailException(
            status=400,
            title="Multiple Images",
            detail="Only one image is allowed per request.",
        )
