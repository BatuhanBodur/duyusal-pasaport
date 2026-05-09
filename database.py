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
    database = load_database()
    if not database:
        return None

    # ID'yi string olarak normalize et
    search_id = str(passport_id).strip()

    # 1. Önce direkt anahtar (key) olarak ara
    if search_id in database:
        return database[search_id]

    # 2. Eğer anahtar olarak yoksa, kayıtların içine bak (farklı alan adları için)
    for record_id, record in database.items():
        # Kayıt içindeki olası ID alanlarını kontrol et
        pid = record.get("pasaport_id") or record.get("passport_id") or record.get("id")
        if str(pid).strip() == search_id:
            return record

    return None