from pydantic import BaseModel


class LicensePlateResponse(BaseModel):
    license_plate: str
