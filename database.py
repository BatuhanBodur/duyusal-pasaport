import streamlit as st
from supabase import create_client


def get_supabase_client():
    """
    Supabase bağlantısını oluşturur.
    Bilgiler .streamlit/secrets.toml veya Streamlit Cloud Secrets içinden okunur.
    """
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def save_passport(passport):
    """
    Yeni pasaport/hasta kaydını Supabase passports tablosuna kaydeder.
    Bu fonksiyon sadece gelen veriyi yazar, yeni ID üretmez.
    """
    supabase = get_supabase_client()

    # ID kontrolü
    passport_id = (
        passport.get("pasaport_id")
        or passport.get("passport_id")
        or passport.get("id")
    )

    if not passport_id:
        raise ValueError("Pasaport ID bulunamadı. Supabase'e kayıt yapılamaz.")

    passport_id = str(passport_id).strip()
    
    # Veli bilgilerini kontrol et ve ayrıştır
    caregiver = passport.get("veli_bilgileri", {})
    caregiver_name = caregiver.get("ad_soyad", "")
    caregiver_phone = caregiver.get("telefon", "")

    # Supabase'e yazılacak satır (explicit mapping)
    row = {
        "passport_id": passport_id,
        "pasaport_url": passport.get("pasaport_url"),
        "olusturma_tarihi": passport.get("olusturma_tarihi"),
        "hasta_bilgileri": passport.get("hasta_bilgileri", {}),
        "veli_bilgileri": {
            "ad_soyad": str(caregiver_name).strip(),
            "telefon": str(caregiver_phone).strip()
        },
        "iletisim_tercihi": passport.get("iletisim_tercihi"),
        "duyusal_profil": passport.get("duyusal_profil", {}),
        "tetikleyiciler": passport.get("tetikleyiciler", []),
        "sakinlestirici_yontemler": passport.get("sakinlestirici_yontemler", []),
        "risk_skoru": passport.get("risk_skoru"),
        "risk_seviyesi": passport.get("risk_seviyesi"),
        "risk_css": passport.get("risk_css"),
        "personel_onerileri": passport.get("personel_onerileri", []),
        "ek_notlar": passport.get("ek_notlar", "")
    }

    # Kaydet (Upsert: Aynı ID varsa günceller, yoksa ekler)
    supabase.table("passports").upsert(row).execute()

    return passport_id


def find_passport_by_id(passport_id):
    """
    QR'dan gelen passport_id ile Supabase'den kayıt çeker.
    Kayıt varsa dict olarak döndürür, yoksa None döndürür.
    """
    supabase = get_supabase_client()

    target_id = str(passport_id).strip()

    if not target_id:
        return None

    response = (
        supabase
        .table("passports")
        .select("*")
        .eq("passport_id", target_id)
        .limit(1)
        .execute()
    )

    if response.data and len(response.data) > 0:
        row = response.data[0]

        return {
            "pasaport_id": row.get("passport_id"),
            "pasaport_url": row.get("pasaport_url"),
            "olusturma_tarihi": row.get("olusturma_tarihi"),
            "hasta_bilgileri": row.get("hasta_bilgileri") or {},
            "veli_bilgileri": row.get("veli_bilgileri") or {},
            "iletisim_tercihi": row.get("iletisim_tercihi"),
            "duyusal_profil": row.get("duyusal_profil") or {},
            "tetikleyiciler": row.get("tetikleyiciler") or [],
            "sakinlestirici_yontemler": row.get("sakinlestirici_yontemler") or [],
            "risk_skoru": row.get("risk_skoru"),
            "risk_seviyesi": row.get("risk_seviyesi"),
            "risk_css": row.get("risk_css"),
            "personel_onerileri": row.get("personel_onerileri") or [],
            "ek_notlar": row.get("ek_notlar") or ""
        }

    return None