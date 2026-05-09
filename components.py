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
        st.markdown("""
        <div class="custom-card">
            <div class="section-title">1. Kayıt</div>
            <div class="soft-text">Hasta / veli bilgileri sisteme girilir.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="custom-card">
            <div class="section-title">2. Duyusal Profil</div>
            <div class="soft-text">Ses, ışık, dokunma, kalabalık ve bekleme hassasiyeti belirlenir.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="custom-card">
            <div class="section-title">3. QR Pasaport</div>
            <div class="soft-text">Hastane personeli QR kod ile dijital pasaport bağlantısına ulaşır.</div>
        </div>
        """, unsafe_allow_html=True)


def render_pills(items):
    if not items:
        st.write("Belirtilmedi.")
        return

    html = "".join(
        f"<span class='mini-pill'>{escape(str(item))}</span>"
        for item in items
    )

    st.markdown(html, unsafe_allow_html=True)


def render_profile_summary(profile):
    profile_items = [
        {"label": "Ses Hassasiyeti", "score": profile["ses_hassasiyeti"], "desc": "Gürültü ve ani seslere duyarlılık"},
        {"label": "Işık Hassasiyeti", "score": profile["isik_hassasiyeti"], "desc": "Parlak ışık ve aydınlatmaya duyarlılık"},
        {"label": "Dokunma Hassasiyeti", "score": profile["dokunma_hassasiyeti"], "desc": "Fiziksel temas ve muayeneye duyarlılık"},
        {"label": "Kalabalık Hassasiyeti", "score": profile["kalabalik_hassasiyeti"], "desc": "İnsan yoğunluğu ve kalabalık ortamdan etkilenme"},
        {"label": "Bekleme Toleransı", "score": profile["bekleme_toleransi_dusuklugu"], "desc": "Uzun bekleme süresine karşı tolerans düşüklüğü"},
    ]

    rows = []
    for item in profile_items:
        label = escape(str(item["label"]))
        score = int(item["score"])
        desc = escape(str(item["desc"]))
        width_percent = int((score / 5) * 100)

        row = (
            "<div class='profile-row'>"
            "<div class='profile-top'>"
            f"<div class='profile-label'>{label}</div>"
            f"<div class='profile-score'>{score}/5</div>"
            "</div>"
            "<div class='profile-bar'>"
            f"<div class='profile-fill' style='width:{width_percent}%;'></div>"
            "</div>"
            f"<div class='profile-desc'>{desc}</div>"
            "</div>"
        )
        rows.append(row)

    html = "<div class='profile-card'>" + "".join(rows) + "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_general_overview(passport):
    patient = passport["hasta_bilgileri"]
    caregiver = passport["veli_bilgileri"]
    profile = passport["duyusal_profil"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pasaport ID", passport["pasaport_id"])
    col2.metric("Risk Skoru", f"{passport['risk_skoru']} / 5")
    col3.metric("Tetikleyici Sayısı", len(passport["tetikleyiciler"]))
    col4.metric("Destekleyici Yöntem", len(passport["sakinlestirici_yontemler"]))

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown(f"""
        <div class="custom-card">
            <div class="section-title">👤 Birey Özeti</div>
            <p><b>Ad Soyad:</b> {escape(str(patient["ad_soyad"]))}</p>
            <p><b>Yaş:</b> {patient["yas"]}</p>
            <p><b>Durum:</b> {escape(str(patient["durum"]))}</p>
            <p><b>Veli / Refakatçi:</b> {escape(str(caregiver["ad_soyad"]))}</p>
            <p><b>Telefon:</b> {escape(str(caregiver["telefon"])) if caregiver["telefon"] else "Belirtilmedi"}</p>
            <p><b>İletişim Tercihi:</b> {escape(str(passport["iletisim_tercihi"]))}</p>
            <p><b>Risk Seviyesi:</b> 
                <span class="{passport["risk_css"]}">{passport["risk_seviyesi"]} Risk</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("### 📈 Duyusal Profil Özeti")
            render_profile_summary(profile)

    with right:
        st.markdown("<div class='custom-card'><div class='section-title'>⚠️ Tetikleyiciler</div></div>", unsafe_allow_html=True)
        render_pills(passport["tetikleyiciler"])
        st.markdown("<br><div class='custom-card'><div class='section-title'>🧩 Destekleyici Yöntemler</div></div>", unsafe_allow_html=True)
        render_pills(passport["sakinlestirici_yontemler"])
        st.markdown("<br><div class='custom-card'><div class='section-title'>📝 Ek Notlar</div></div>", unsafe_allow_html=True)
        st.write(passport["ek_notlar"] if passport["ek_notlar"] else "Ek not girilmedi.")


def render_digital_passport(passport, create_qr_code_func):
    patient = passport["hasta_bilgileri"]
    passport_url = get_passport_url(passport)
    qr_png_bytes = create_qr_code_func(passport_url)

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(f"""
        <div class="custom-card">
            <div class="section-title">🪪 Dijital Pasaport Kartı</div>
            <p><b>Pasaport ID:</b> {passport["pasaport_id"]}</p>
            <p><b>Ad Soyad:</b> {escape(str(patient["ad_soyad"]))}</p>
            <p><b>Yaş:</b> {patient["yas"]}</p>
            <p><b>Tanı / Durum:</b> {escape(str(patient["durum"]))}</p>
            <p><b>Risk Durumu:</b> 
                <span class="{passport["risk_css"]}">{passport["risk_seviyesi"]} Risk</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='custom-card'><div class='section-title'>💡 Hızlı Özet</div></div>", unsafe_allow_html=True)
        st.markdown("**Tetikleyiciler**")
        render_pills(passport["tetikleyiciler"])
        st.markdown("**Destekleyici Yöntemler**")
        render_pills(passport["sakinlestirici_yontemler"])

    with right:
        st.markdown("<div class='custom-card'><div class='section-title'>📱 QR Kod</div></div>", unsafe_allow_html=True)
        st.image(qr_png_bytes, width=300)
        st.download_button("QR Kodu İndir", qr_png_bytes, f"qr_{passport['pasaport_id']}.png", "image/png")
        st.download_button("JSON İndir", to_json_bytes(passport), f"pasaport_{passport['pasaport_id']}.json", "application/json")


def render_staff_panel(passport, is_read_only=False):
    patient = passport["hasta_bilgileri"]

    st.markdown(f"""
    <div class="custom-card">
        <div class="section-title">👩‍⚕️ Personel İçin Hızlı Bilgilendirme</div>
        <p><b>Hasta:</b> {escape(str(patient["ad_soyad"]))}</p>
        <p><b>Yaş:</b> {patient["yas"]}</p>
        <p><b>Tanı / Durum:</b> {escape(str(patient["durum"]))}</p>
        <p><b>Risk Durumu:</b> 
            <span class="{passport["risk_css"]}">{passport["risk_seviyesi"]} Risk</span>
        </p>
        <p><b>İletişim Şekli:</b> {escape(str(passport["iletisim_tercihi"]))}</p>
    </div>
    """, unsafe_allow_html=True)

    if passport["risk_seviyesi"] == "Yüksek":
        st.markdown("<div class='danger-box'><b>Yüksek risk:</b> Sakin alan ve hızlı yönlendirme önerilir.</div>", unsafe_allow_html=True)
    elif passport["risk_seviyesi"] == "Orta":
        st.markdown("<div class='warning-box'><b>Orta risk:</b> Duyusal uyaranlar kontrollü yönetilmelidir.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='success-box'><b>Düşük risk:</b> Standart süreç uygulanabilir.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='custom-card'><div class='section-title'>⚠️ Tetikleyiciler</div></div>", unsafe_allow_html=True)
        render_pills(passport["tetikleyiciler"])
    with col2:
        st.markdown("<div class='custom-card'><div class='section-title'>🧩 Destekleyici Uygulamalar</div></div>", unsafe_allow_html=True)
        render_pills(passport["sakinlestirici_yontemler"])

    st.markdown("<br><div class='custom-card'><div class='section-title'>✅ Personel Önerileri</div></div>", unsafe_allow_html=True)
    for rec in passport["personel_onerileri"]:
        st.markdown(f"<div class='recommend-box'>• {escape(str(rec))}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    staff_note = f"Hasta {patient['ad_soyad']}, {passport['risk_seviyesi'].lower()} düzeyde duyusal hassasiyet gösterebilir.\nİletişim: {passport['iletisim_tercihi']}.\nTetikleyiciler: {', '.join(passport['tetikleyiciler'])}.\nÖneri: sakin alan, kısa açıklama."
    st.text_area("Kopyalanabilir Personel Notu", value=staff_note, height=150, disabled=is_read_only)


def render_qr_personnel_panel(passport):
    """
    QR kod ile gelen kullanıcıya (sağlık personeli) doğrudan gösterilen read-only ekran.
    """
    patient = passport["hasta_bilgileri"]
    caregiver = passport["veli_bilgileri"]
    
    render_hero()
    st.success(f"🔍 Duyusal Pasaport Görüntüleme Modu: {passport['pasaport_id']}")
    
    # Ana Bilgi Kartı
    st.markdown(f"""
    <div class="custom-card">
        <div class="section-title">👩‍⚕️ Hızlı Hasta Özeti</div>
        <div style="font-size: 1.1rem; line-height: 1.8;">
            <p><b>Ad Soyad:</b> {escape(str(patient["ad_soyad"]))}</p>
            <p><b>Yaş:</b> {patient["yas"]}</p>
            <p><b>Tanı / Durum:</b> {escape(str(patient["durum"]))}</p>
            <p><b>Risk Durumu:</b> <span class="{passport["risk_css"]}">{passport["risk_seviyesi"]} Risk</span> (Skor: {passport["risk_skoru"]}/5)</p>
            <p><b>İletişim Tercihi:</b> {escape(str(passport["iletisim_tercihi"]))}</p>
            <p><b>Veli / Refakatçi:</b> {escape(str(caregiver["ad_soyad"]))} ({escape(str(caregiver["telefon"]))})</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detay Kartları
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='custom-card'><div class='section-title'>⚠️ Tetikleyiciler</div></div>", unsafe_allow_html=True)
        render_pills(passport["tetikleyiciler"])
        
        st.markdown("<br><div class='custom-card'><div class='section-title'>🧩 Destekleyici Yöntemler</div></div>", unsafe_allow_html=True)
        render_pills(passport["sakinlestirici_yontemler"])

    with col2:
        st.markdown("<div class='custom-card'><div class='section-title'>📈 Duyusal Profil</div></div>", unsafe_allow_html=True)
        render_profile_summary(passport["duyusal_profil"])

    st.markdown("<br><div class='custom-card'><div class='section-title'>✅ Uygulanması Önerilen Adımlar</div></div>", unsafe_allow_html=True)
    for rec in passport["personel_onerileri"]:
        st.markdown(f"<div class='recommend-box'>• {escape(str(rec))}</div>", unsafe_allow_html=True)

    if passport["ek_notlar"]:
        st.markdown(f"<br><div class='custom-card'><div class='section-title'>📝 Ek Notlar</div><p>{escape(str(passport['ek_notlar']))}</p></div>", unsafe_allow_html=True)

    # QR Kaynak (MediaFileHandler hatası almamak için anlık üretim)
    st.markdown("---")
    qr_bytes = create_qr_code(generate_qr_url(passport["pasaport_id"]))
    st.image(qr_bytes, width=150, caption="Pasaport QR Kaynağı")