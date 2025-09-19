import qrcode
from io import BytesIO

def generate_qr(content):
    img = qrcode.make(content)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
