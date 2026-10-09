from errors import ProblemDetail, ProblemDetailException

PROBLEM_JSON = "application/problem+json"


def problem_response(description: str, instance: str, *errors: ProblemDetailException) -> dict:
    """Builds an OpenAPI response with one example per error, taken from the real error factories."""
    examples = {
        error.title: {
            "summary": error.title,
            "value": ProblemDetail(
                type=error.type,
                title=error.title,
                status=error.status,
                detail=error.detail,
                instance=instance,
            ).model_dump(),
        }
        for error in errors
    }
    return {
        "description": description,
        "content": {
            PROBLEM_JSON: {
                "schema": ProblemDetail.model_json_schema(),
                "examples": examples,
            }
        },
    }
