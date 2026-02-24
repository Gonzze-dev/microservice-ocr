from starlette.datastructures import FormData

from errors import LicensePlateErrors


def validate_platform_code(platform_code: str):
    if platform_code is None or platform_code == "":
        raise LicensePlateErrors.platform_code_is_required()


def validate_single_image(form: FormData):
    file_count = 0
    for _, v in form.multi_items():
        if hasattr(v, "filename"):
            file_count += 1
            if file_count > 1:
                raise LicensePlateErrors.multiple_images()
