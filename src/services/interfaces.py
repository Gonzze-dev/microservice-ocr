from abc import ABC, abstractmethod
from numpy import ndarray


class ILicensePlateDetector(ABC):
    @abstractmethod
    def get_license_plate_image(self, image) -> ndarray:
        ...


class IOCR(ABC):
    @abstractmethod
    def get_license_plate_text(self, image) -> str:
        ...
