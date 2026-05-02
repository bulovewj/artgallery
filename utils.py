import json
import os
from pathlib import Path

DATA_FILE = "data/paintings.json"
CONTACT_FILE = "data/contact.json"

def ensure_data_dir():
    Path("data").mkdir(exist_ok=True)
    Path("assets/paintings").mkdir(parents=True, exist_ok=True)

def load_paintings():
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_paintings(paintings):
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(paintings, f, ensure_ascii=False, indent=2)

def get_contact_info():
    ensure_data_dir()
    default = {
        "phone": "010-0000-0000",
        "instagram": "@your_instagram",
        "intro": "꽃과 풍경을 담은 원화를 판매합니다.\n구매 문의는 전화 또는 인스타그램 DM으로 연락 주세요."
    }
    if not os.path.exists(CONTACT_FILE):
        return default
    with open(CONTACT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {**default, **data}

def save_contact_info(info):
    ensure_data_dir()
    with open(CONTACT_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

def get_categories(paintings):
    cats = set()
    for p in paintings:
        if p.get("category"):
            cats.add(p["category"])
    return sorted(list(cats))
