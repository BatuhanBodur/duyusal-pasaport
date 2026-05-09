import json
from html import escape
import streamlit as st
from qr_utils import get_passport_url, create_qr_code, generate_qr_url


def to_json_bytes(data):
    return json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8")


def render_hero():
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🪪 Duyusal Pasaport</div>
        <div class="hero-subtitle">
            Hastane Deneyim Kişiselleştirme Modeli · Otizmli ve duyusal hassasiyeti olan bireyler için
            daha sakin, daha güvenli ve daha yönetilebilir hastane süreci.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_intro_cards():
    st.markdown("""
    <div class="custom-card">
        <div class="section-title">Hoş geldin 👋</div>
        <div class="soft-text">
            Sol menüden birey, veli ve duyusal profil bilgilerini doldur.
            Sistem otomatik olarak risk düzeyi, öneriler ve QR kodlu dijital pasaport oluşturacaktır.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='custom-card'><div class='section-title'>1. Kayıt</div><div class='soft-text'>Hasta / veli bilgileri sisteme girilir.</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='custom-card'><div class='section-title'>2. Duyusal Profil</div><div class='soft-text'>Hassasiyetler belirlenir.</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='custom-card'><div class='section-title'>3. QR Pasaport</div><div class='soft-text'>Personel QR kod ile bilgilere ulaşır.</div></div>", unsafe_allow_html=True)


def render_pills(items):
    if not items:
        st.write("Belirtilmedi.")
        return
    html = "".join(f"<span class='mini-pill'>{escape(str(item))}</span>" for item in items)
    st.markdown(html, unsafe_allow_html=True)


def render_profile_summary(profile):
    profile_items = [
        {"label": "Ses Hassasiyeti", "score": profile["ses_hassasiyeti"], "desc": "Gürültüye duyarlılık"},
        {"label": "Işık Hassasiyeti", "score": profile["isik_hassasiyeti"], "desc": "Işığa duyarlılık"},
        {"label": "Dokunma Hassasiyeti", "score": profile["dokunma_hassasiyeti"], "desc": "Temasa duyarlılık"},
        {"label": "Kalabalık Hassasiyeti", "score": profile["kalabalik_hassasiyeti"], "desc": "Kalabalığa duyarlılık"},
        {"label": "Bekleme Toleransı", "score": profile["bekleme_toleransi_dusuklugu"], "desc": "Bekleme sabrı"},
    ]
    rows = []
    for item in profile_items:
        score = int(item["score"])
        width = int((score / 5) * 100)
        row = f"<div class='profile-row'><div class='profile-top'><div class='profile-label'>{item['label']}</div><div class='profile-score'>{score}/5</div></div><div class='profile-bar'><div class='profile-fill' style='width:{width}%;'></div></div></div>"
        rows.append(row)
    st.markdown("<div class='profile-card'>" + "".join(rows) + "</div>", unsafe_allow_html=True)


def render_staff_panel(passport, is_read_only=False):
    patient = passport["hasta_bilgileri"]
    st.markdown(f"""
    <div class="custom-card">
        <div class="section-title">👩‍⚕️ Personel İçin Hızlı Bilgilendirme</div>
        <p><b>Hasta:</b> {escape(str(patient["ad_soyad"]))}</p>
        <p><b>Yaş:</b> {patient["yas"]}</p>
        <p><b>Tanı / Durum:</b> {escape(str(patient["durum"]))}</p>
        <p><b>Risk Durumu:</b> <span class="{passport["risk_css"]}">{passport["risk_seviyesi"]} Risk</span></p>
        <p><b>İletişim Şekli:</b> {escape(str(passport["iletisim_tercihi"]))}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='custom-card'><div class='section-title'>⚠️ Tetikleyiciler</div></div>", unsafe_allow_html=True)
        render_pills(passport["tetikleyiciler"])
    with col2:
        st.markdown("<div class='custom-card'><div class='section-title'>🧩 Destekleyici Uygulamalar</div></div>", unsafe_allow_html=True)
        render_pills(passport["sakinlestirici_yontemler"])

    st.markdown("<br><div class='custom-card'><div class='section-title'>✅ Uygulanması Önerilen Adımlar</div></div>", unsafe_allow_html=True)
    for rec in passport["personel_onerileri"]:
        st.markdown(f"<div class='recommend-box'>• {escape(str(rec))}</div>", unsafe_allow_html=True)

    staff_note = f"Hasta {patient['ad_soyad']}, {passport['risk_seviyesi'].lower()} risk grubundadır.\nİletişim: {passport['iletisim_tercihi']}.\nTetikleyiciler: {', '.join(passport['tetikleyiciler'])}."
    st.text_area("Kopyalanabilir Personel Notu", value=staff_note, height=150, disabled=is_read_only)


def render_qr_personnel_panel(passport):
    """
    QR Modu için özel, read-only ve eksiksiz personel ekranı.
    """
    patient = passport["hasta_bilgileri"]
    caregiver = passport["veli_bilgileri"]
    
    render_hero()
    st.success(f"🔍 Duyusal Pasaport Görüntüleme Modu: {passport['pasaport_id']}")
    
    # 1. Hızlı Özet
    st.markdown(f"""
    <div class="custom-card">
        <div class="section-title">👩‍⚕️ Hızlı Hasta Özeti</div>
        <div style="font-size: 1.1rem; line-height: 1.8;">
            <p><b>Ad Soyad:</b> {escape(str(patient["ad_soyad"]))}</p>
            <p><b>Yaş:</b> {patient["yas"]}</p>
            <p><b>Tanı / Durum:</b> {escape(str(patient["durum"]))}</p>
            <p><b>Risk Durumu:</b> <span class="{passport["risk_css"]}">{passport["risk_seviyesi"]} Risk</span> (Skor: {passport["risk_skoru"]}/5)</p>
            <p><b>İletişim Tercihi:</b> {escape(str(passport["iletisim_tercihi"]))}</p>
            <p><b>Veli / Refakatçi:</b> {escape(str(caregiver["ad_soyad"]))} - {escape(str(caregiver.get("telefon", "Belirtilmedi")))}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Detaylı Bilgi
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='custom-card'><div class='section-title'>⚠️ Tetikleyiciler</div></div>", unsafe_allow_html=True)
        render_pills(passport["tetikleyiciler"])
        st.markdown("<br><div class='custom-card'><div class='section-title'>🧩 Destekleyici Uygulamalar</div></div>", unsafe_allow_html=True)
        render_pills(passport["sakinlestirici_yontemler"])

    with col2:
        st.markdown("<div class='custom-card'><div class='section-title'>📈 Duyusal Profil</div></div>", unsafe_allow_html=True)
        render_profile_summary(passport["duyusal_profil"])

    # 3. Öneriler ve Notlar
    st.markdown("<br><div class='custom-card'><div class='section-title'>✅ Uygulanması Önerilen Adımlar</div></div>", unsafe_allow_html=True)
    for rec in passport["personel_onerileri"]:
        st.markdown(f"<div class='recommend-box'>• {escape(str(rec))}</div>", unsafe_allow_html=True)

    if passport["ek_notlar"]:
        st.markdown(f"<br><div class='custom-card'><div class='section-title'>📝 Ek Notlar</div><p>{escape(str(passport['ek_notlar']))}</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    qr_bytes = create_qr_code(generate_qr_url(passport["pasaport_id"]))
    st.image(qr_bytes, width=150, caption="Pasaport Doğrulama QR")


def render_general_overview(passport):
    patient = passport["hasta_bilgileri"]
    caregiver = passport["veli_bilgileri"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pasaport ID", passport["pasaport_id"])
    col2.metric("Risk Skoru", f"{passport['risk_skoru']} / 5")
    col3.metric("Tetikleyici", len(passport["tetikleyiciler"]))
    col4.metric("Destekleyici", len(passport["sakinlestirici_yontemler"]))
    
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown(f"<div class='custom-card'><div class='section-title'>👤 Birey Özeti</div><p><b>Ad Soyad:</b> {escape(str(patient['ad_soyad']))}</p><p><b>Yaş:</b> {patient['yas']}</p><p><b>Durum:</b> {escape(str(patient['durum']))}</p></div>", unsafe_allow_html=True)
        render_profile_summary(passport["duyusal_profil"])
    with right:
        st.markdown("<div class='custom-card'><div class='section-title'>⚠️ Tetikleyiciler</div></div>", unsafe_allow_html=True)
        render_pills(passport["tetikleyiciler"])
        st.markdown("<br><div class='custom-card'><div class='section-title'>🧩 Destekleyici Yöntemler</div></div>", unsafe_allow_html=True)
        render_pills(passport["sakinlestirici_yontemler"])


def render_digital_passport(passport, create_qr_code_func):
    patient = passport["hasta_bilgileri"]
    passport_url = get_passport_url(passport)
    qr_png_bytes = create_qr_code_func(passport_url)
    
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown(f"<div class='custom-card'><div class='section-title'>🪪 Dijital Pasaport Kartı</div><p><b>ID:</b> {passport['pasaport_id']}</p><p><b>Ad Soyad:</b> {escape(str(patient['ad_soyad']))}</p><p><b>Yaş:</b> {patient['yas']}</p><p><b>Risk Seviyesi:</b> <span class='{passport['risk_css']}'>{passport['risk_seviyesi']} Risk</span></p></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='custom-card'><div class='section-title'>📱 QR Kod</div></div>", unsafe_allow_html=True)
        st.image(qr_png_bytes, width=300)
        st.download_button("QR Kodu İndir", qr_png_bytes, f"qr_{passport['pasaport_id']}.png", "image/png")