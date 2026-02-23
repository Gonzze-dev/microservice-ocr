from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ProblemDetail(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: str | None = None


class ProblemDetailException(Exception):
    def __init__(
        self,
        status: int,
        title: str,
        detail: str,
        type: str = "about:blank",
        instance: str | None = None,
    ):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = type
        self.instance = instance


async def problem_detail_handler(request: Request, exc: ProblemDetailException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content=ProblemDetail(
            type=exc.type,
            title=exc.title,
            status=exc.status,
            detail=exc.detail,
            instance=exc.instance or str(request.url),
        ).model_dump(),
        media_type="application/problem+json",
    )
