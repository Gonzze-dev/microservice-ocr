from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ALLOWED_ORIGINS
from routers import license_plate_router, health_router
from services import LicensePlateDetector, OCR
from errors import ProblemDetailException, problem_detail_handler
import uvicorn

app = FastAPI(title="Microservice OCR - License Plate Reader")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ProblemDetailException, problem_detail_handler)

app.state.license_plate_detector = LicensePlateDetector()
app.state.ocr = OCR()

app.include_router(health_router)
app.include_router(license_plate_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
