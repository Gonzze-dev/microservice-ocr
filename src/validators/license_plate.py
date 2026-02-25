from starlette.datastructures import FormData

from errors import LicensePlateErrors


def validate_single_image(form: FormData):
    file_count = 0
    for _, v in form.multi_items():
        if hasattr(v, "filename"):
            file_count += 1
            if file_count > 1:
                raise LicensePlateErrors.multiple_images()
