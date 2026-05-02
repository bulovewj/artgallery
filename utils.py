import json
import os
from pathlib import Path

DATA_FILE = "data/paintings.json"
CONTACT_FILE = "data/contact.json"
TEXTS_FILE = "data/texts.json"

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
        return {**default, **json.load(f)}

def save_contact_info(info):
    ensure_data_dir()
    with open(CONTACT_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

def get_site_texts():
    ensure_data_dir()
    default = {
        "site_title": "Atelier",
        "site_subtitle": "꽃과 풍경, 그리고 따뜻한 시간",
        "site_tagline": "Original Paintings · Handmade with Love",
        "intro_line1": "일상에 꽃 한 송이, 풍경 한 폭을 들이세요.",
        "intro_line2": "모든 작품은 직접 그린 원화입니다.",
        "cta_title": "마음에 드는 작품이 있으신가요?",
        "cta_sub": "구매 문의는 아래 연락처로 편하게 연락 주세요",
        "footer_text": "© 2025 Atelier · All artworks are original and handmade · 무단 복제 및 배포 금지",
    }
    if not os.path.exists(TEXTS_FILE):
        return default
    with open(TEXTS_FILE, "r", encoding="utf-8") as f:
        return {**default, **json.load(f)}

def save_site_texts(texts):
    ensure_data_dir()
    with open(TEXTS_FILE, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

def get_categories(paintings):
    cats = set()
    for p in paintings:
        if p.get("category"):
            cats.add(p["category"])
    return sorted(list(cats))
