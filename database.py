import json
import os

# Veritabanı dosya yolu (Relative path / Deployment safe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "duyusal_pasaport_veritabani.json")


def load_database():
    """
    JSON veritabanını okur.
    Dosya yoksa boş sözlük döndürür.
    """

    if not os.path.exists(DB_PATH):
        return {}

    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_database(database):
    """
    Veritabanını JSON dosyasına yazar.
    """

    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(database, file, ensure_ascii=False, indent=4)


def save_passport_to_database(passport):
    """
    Oluşturulan duyusal pasaportu pasaport ID üzerinden kaydeder.
    """

    database = load_database()
    database[passport["pasaport_id"]] = passport
    save_database(database)


def get_passport_from_database(passport_id):
    """
    QR koddan gelen passport_id ile kayıtlı pasaportu bulur.
    """

    database = load_database()
    return database.get(passport_id)


def find_passport_by_id(passport_id):
    """
    JSON veritabanında passport_id ile kayıt ara.
    Hem anahtar olarak hem de kayıt içindeki alanlar olarak kontrol eder.
    """
    data = load_database()
    target_id = str(passport_id).strip()

    if not target_id:
        return None

    # Eğer data dict ise
    if isinstance(data, dict):
        # 1. Önce direkt anahtar (key) olarak ara
        if target_id in data and isinstance(data[target_id], dict):
            return data[target_id]

        # 2. Eğer anahtar olarak yoksa, kayıtların içine bak
        for record in data.values():
            if isinstance(record, dict):
                record_id = (
                    record.get("pasaport_id")
                    or record.get("passport_id")
                    or record.get("id")
                )
                if str(record_id).strip() == target_id:
                    return record

    # Eğer data list ise (eski/alternatif yapı desteği)
    if isinstance(data, list):
        for record in data:
            if isinstance(record, dict):
                record_id = (
                    record.get("pasaport_id")
                    or record.get("passport_id")
                    or record.get("id")
                )
                if str(record_id).strip() == target_id:
                    return record

    return None