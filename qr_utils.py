import qrcode
from io import BytesIO
import streamlit as st

# Streamlit Cloud Deployment için Base URL
# GitHub'a yükledikten sonra burayı kendi uygulama linkinizle değiştirin.
BASE_URL = "https://senin-uygulama-linkin.streamlit.app"

def generate_qr_url(passport_id):
    """
    QR içine yazılacak pasaport linkini üretir.
    Deployment sonrası BASE_URL üzerinden çalışır.
    """
    return f"{BASE_URL}?passport_id={passport_id}"


def get_passport_url(passport):
    """
    Pasaport verisinin içindeki URL varsa onu döndürür.
    Yoksa güncel BASE_URL ile yeniden üretir.
    """

    if "pasaport_url" in passport and passport["pasaport_url"] and not passport["pasaport_url"].startswith("http://localhost"):
        return passport["pasaport_url"]

    return generate_qr_url(passport["pasaport_id"])


def create_qr_code(qr_text):
    """
    Verilen bağlantıyı QR koda çevirir.
    Geriye PNG byte verisi döndürür.
    """

    qr = qrcode.QRCode(
        version=3,
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