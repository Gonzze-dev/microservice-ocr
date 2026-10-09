from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, RedirectResponse

from docs import HEALTH_RESPONSES

router = APIRouter(tags=["Health"])


@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/health")


@router.get(
    "/health",
    response_class=PlainTextResponse,
    summary="Health check",
    description="Verifica que el servicio esté en funcionamiento. No requiere autenticación.",
    responses=HEALTH_RESPONSES,
    openapi_extra={"security": []},
)
async def health_check():
    return "OK"
