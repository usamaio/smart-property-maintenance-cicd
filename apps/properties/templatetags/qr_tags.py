import base64
from io import BytesIO

import qrcode
from django import template


register = template.Library()


@register.simple_tag
def qr_code_data_uri(request, relative_url):
    """
    Generate a PNG QR code as an inline data URI.

    The QR code contains an absolute application URL only.
    """
    if request is None or not relative_url:
        return ''

    absolute_url = request.build_absolute_uri(relative_url)

    qr_code = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )

    qr_code.add_data(absolute_url)
    qr_code.make(fit=True)

    image = qr_code.make_image(
        fill_color='black',
        back_color='white',
    )

    image_buffer = BytesIO()
    image.save(
        image_buffer,
        format='PNG',
    )

    encoded_image = base64.b64encode(
        image_buffer.getvalue()
    ).decode('utf-8')

    return f'data:image/png;base64,{encoded_image}'