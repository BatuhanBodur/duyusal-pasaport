import qrcode
from io import BytesIO
from urllib.parse import urlencode


BASE_URL = "https://duyusal-pasaport-batuhan.streamlit.app"


def generate_qr_url(passport_id):
    """
    QR içine yazılacak pasaport linkini üretir.
    """
    if passport_id is None or str(passport_id).strip() == "":
        raise ValueError("passport_id boş olamaz.")

    query = urlencode({"passport_id": str(passport_id)})
    return f"{BASE_URL}?{query}"


def get_passport_url(passport):
    """
    Her zaman güncel canlı link üretir, JSON içindeki eski verilere güvenmez.
    """
    passport_id = (
        passport.get("pasaport_id")
        or passport.get("passport_id")
        or passport.get("id")
    )

    if not passport_id:
        raise ValueError("Pasaport ID bulunamadı.")

    return generate_qr_url(passport_id)


def create_qr_code(qr_text):
    """
    Verilen metni QR koda çevirir.
    """
    if qr_text is None or str(qr_text).strip() == "":
        raise ValueError("QR kod metni boş olamaz.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=9,
        border=3
    )

    qr.add_data(str(qr_text))
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()