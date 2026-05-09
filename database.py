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