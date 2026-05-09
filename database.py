import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "duyusal_pasaport_veritabani.json")


def load_database():
    if not os.path.exists(DB_PATH):
        return {}

    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except (json.JSONDecodeError, Exception):
        return {}


def save_database(data):
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_passport(passport):
    data = load_database()

    passport_id = (
        passport.get("pasaport_id")
        or passport.get("passport_id")
        or passport.get("id")
    )

    if not passport_id:
        raise ValueError("Pasaport ID bulunamadı. JSON'a kayıt yapılamaz.")

    passport_id = str(passport_id).strip()
    passport["pasaport_id"] = passport_id

    data[passport_id] = passport
    save_database(data)

    return passport_id


def find_passport_by_id(passport_id):
    data = load_database()
    target_id = str(passport_id).strip()

    if not target_id:
        return None

    if isinstance(data, dict):
        # 1. Direkt anahtar olarak ara
        if target_id in data and isinstance(data[target_id], dict):
            return data[target_id]

        # 2. Kayıtların içinde ara
        for record in data.values():
            if isinstance(record, dict):
                record_id = (
                    record.get("pasaport_id")
                    or record.get("passport_id")
                    or record.get("id")
                )

                if str(record_id).strip() == target_id:
                    return record

    return None

# Uyumluluk için eski fonksiyon isimleri
def get_passport_from_database(passport_id):
    return find_passport_by_id(passport_id)

def save_passport_to_database(passport):
    return save_passport(passport)