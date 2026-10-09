from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, RedirectResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/health")


@router.get("/health", response_class=PlainTextResponse)
async def health_check():
    return "OK"
