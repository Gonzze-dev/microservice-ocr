from errors.exceptions import ProblemDetailException


class AuthErrors:
    @staticmethod
    def invalid_api_key() -> ProblemDetailException:
        return ProblemDetailException(
            status=401,
            title="Unauthorized",
            detail="The provided API key is invalid or missing.",
        )
