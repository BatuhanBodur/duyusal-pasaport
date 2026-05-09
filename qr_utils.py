import qrcode
from io import BytesIO
from urllib.parse import urlencode


BASE_URL = "https://duyusal-pasaport-batuhan.streamlit.app"


def generate_qr_url(passport_id):
    """
    QR içine yazılacak pasaport linkini üretir.
    Canlı Streamlit URL'si üzerinden çalışır.
    Örnek çıktı:
    https://duyusal-pasaport-batuhan.streamlit.app?passport_id=123
    """

    if passport_id is None or str(passport_id).strip() == "":
        raise ValueError("passport_id boş olamaz.")

    query = urlencode({"passport_id": str(passport_id)})
    return f"{BASE_URL}?{query}"


def get_passport_url(passport):
    """
    Pasaport verisi için güncel canlı URL üretir.
    JSON içinde eski localhost / local IP / placeholder URL olsa bile onu kullanmaz.
    """

    passport_id = passport.get("pasaport_id") or passport.get("passport_id")

    if passport_id is None:
        raise KeyError("Pasaport verisinde 'pasaport_id' alanı bulunamadı.")

    return generate_qr_url(passport_id)


def create_qr_code(qr_text):
    """
    Verilen bağlantıyı QR koda çevirir.
    Geriye PNG byte verisi döndürür.
    Streamlit içinde st.image(...) ile gösterilebilir.
    """

    if qr_text is None or str(qr_text).strip() == "":
        raise ValueError("QR kod oluşturmak için bağlantı boş olamaz.")

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