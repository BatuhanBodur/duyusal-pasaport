import streamlit as st
from datetime import datetime
import uuid
from html import escape

from styles import apply_styles
from database import save_passport_to_database, get_passport_from_database
from qr_utils import (
    create_qr_code,
    generate_qr_url
)
from risk_engine import calculate_risk
from recommendations import generate_recommendations
from components import (
    render_hero,
    render_intro_cards,
    render_pills,
    render_general_overview,
    render_digital_passport,
    render_staff_panel
)


# ============================================================
# SAYFA AYARI
# ============================================================

st.set_page_config(
    page_title="Duyusal Pasaport",
    page_icon="🪪",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()


# ============================================================
# SESSION STATE
# ============================================================

if "passport" not in st.session_state:
    st.session_state.passport = None


# ============================================================
# QR İLE GELEN PASAPORTU YÜKLE VE GÖRÜNTÜLE (READ-ONLY MOD)
# ============================================================

# URL parametrelerini oku
params = st.query_params
qr_passport_id = params.get("passport_id", None)

# Eğer URL'de passport_id varsa, uygulama sadece görüntüleme modunda çalışır
if qr_passport_id:
    # Sidebar'ı ve genişletme butonunu CSS ile tamamen gizle (Ekstra güvenlik)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="collapsedControl"] {
                display: none;
            }
            .main .block-container {
                max-width: 1100px;
                padding-left: 2rem;
                padding-right: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    from database import find_passport_by_id
    from components import render_qr_readonly_mode
    
    # Veritabanında ara
    passport_data = find_passport_by_id(qr_passport_id)
    
    if passport_data:
        # Doğrudan özel read-only personel panelini göster
        render_qr_readonly_mode(passport_data)
        
        # Akışı burada durdur! (Sidebar ve kayıt formu kesinlikle render edilmez)
        st.stop()
    else:
        # Kayıt bulunamadıysa hata göster ve dur
        render_hero()
        st.error(f"⚠️ Bu QR koda ait hasta bilgisi bulunamadı: {qr_passport_id}")
        st.stop()


# ============================================================
# ÜST BAŞLIK
# ============================================================

render_hero()


# ============================================================
# SIDEBAR FORM
# ============================================================

with st.sidebar:
    st.markdown("## 🧾 Pasaport Bilgileri")
    st.markdown("Birey ve veli bilgilerini gir.")
    
    with st.form("passport_form"):
        patient_name = st.text_input("Bireyin Adı Soyadı")
        age = st.number_input("Yaş", min_value=1, max_value=100, value=10)

        diagnosis = st.selectbox(
            "Durum / Tanı Bilgisi",
            [
                "Otizm Spektrum Bozukluğu",
                "Duyusal hassasiyet",
                "Özel öğrenme güçlüğü",
                "Zihinsel yetersizlik",
                "Diğer"
            ]
        )

        caregiver_name = st.text_input("Veli / Refakatçi Adı")
        caregiver_phone = st.text_input("Telefon")

        communication = st.selectbox(
            "İletişim Tercihi",
            [
                "Kısa ve net cümleler",
                "Görsel anlatım",
                "Yavaş ve sakin konuşma",
                "Veli aracılığıyla iletişim",
                "Sessiz yönlendirme"
            ]
        )

        st.markdown("---")
        st.markdown("## 🎛️ Duyusal Profil")

        sound = st.slider("Ses Hassasiyeti", 1, 5, 3)
        light = st.slider("Işık Hassasiyeti", 1, 5, 3)
        touch = st.slider("Dokunma Hassasiyeti", 1, 5, 3)
        crowd = st.slider("Kalabalık Hassasiyeti", 1, 5, 3)
        waiting = st.slider("Bekleme Toleransı Düşüklüğü", 1, 5, 3)

        triggers = st.multiselect(
            "Tetikleyici Durumlar",
            [
                "Yüksek ses",
                "Parlak ışık",
                "Kalabalık ortam",
                "İğne / kan alma",
                "Beyaz önlük",
                "Uzun bekleme",
                "Ani temas",
                "Kapalı alan",
                "Bilinmeyen ortam"
            ]
        )

        calming_methods = st.multiselect(
            "Destekleyici / Sakinleştirici Yöntemler",
            [
                "Sessiz alan",
                "Kulaklık",
                "Oyuncak / nesne",
                "Tablet / görsel destek",
                "Veli yanında olmalı",
                "Kısa açıklama yapılmalı",
                "Bekleme süresi azaltılmalı",
                "Loş ışık tercih edilmeli"
            ]
        )

        notes = st.text_area(
            "Ek Notlar",
            placeholder=(
                "Örn: Kalabalıkta huzursuzlanıyor, işlem öncesi kısa açıklama yapılınca rahatlıyor..."
            )
        )

        submitted = st.form_submit_button("Pasaportu Oluştur / Güncelle")

        if submitted:
            if not patient_name.strip() or not caregiver_name.strip():
                st.error("Bireyin adı ve veli / refakatçi adı boş bırakılamaz.")
            else:
                risk_score, risk_level, risk_css = calculate_risk(
                    sound,
                    light,
                    touch,
                    crowd,
                    waiting
                )

                recommendations = generate_recommendations(
                    sound,
                    light,
                    touch,
                    crowd,
                    waiting,
                    triggers,
                    calming_methods
                )

                passport_id = str(uuid.uuid4())[:8].upper()
                passport_url = generate_qr_url(passport_id)

                passport_data = {
                    "pasaport_id": passport_id,
                    "pasaport_url": passport_url,
                    "olusturma_tarihi": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "hasta_bilgileri": {
                        "ad_soyad": patient_name,
                        "yas": age,
                        "durum": diagnosis
                    },
                    "veli_bilgileri": {
                        "ad_soyad": caregiver_name,
                        "telefon": caregiver_phone
                    },
                    "iletisim_tercihi": communication,
                    "duyusal_profil": {
                        "ses_hassasiyeti": sound,
                        "isik_hassasiyeti": light,
                        "dokunma_hassasiyeti": touch,
                        "kalabalik_hassasiyeti": crowd,
                        "bekleme_toleransi_dusuklugu": waiting
                    },
                    "tetikleyiciler": triggers,
                    "sakinlestirici_yontemler": calming_methods,
                    "risk_skoru": risk_score,
                    "risk_seviyesi": risk_level,
                    "risk_css": risk_css,
                    "personel_onerileri": recommendations,
                    "ek_notlar": notes
                }

                st.session_state.passport = passport_data
                save_passport_to_database(passport_data)

                st.success("Pasaport başarıyla oluşturuldu ve kaydedildi.")


# ============================================================
# ANA İÇERİK
# ============================================================

passport = st.session_state.passport

tab1, tab2, tab3 = st.tabs([
    "📊 Genel Görünüm",
    "🪪 Dijital Pasaport",
    "👩‍⚕️ Personel Paneli"
])

with tab1:
    if passport is None:
        render_intro_cards()
    else:
        render_general_overview(passport)

with tab2:
    if passport is None:
        st.info("Önce sol menüden pasaport oluşturmalısın.")
    else:
        render_digital_passport(passport, create_qr_code)

with tab3:
    if passport is None:
        st.info("Önce pasaport oluşturulmalıdır.")
    else:
        render_staff_panel(passport)