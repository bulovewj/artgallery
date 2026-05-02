import json
import os
import base64
import requests
from pathlib import Path

# ── GitHub 설정 (Streamlit secrets에서 읽음) ──
def get_gh_config():
    try:
        import streamlit as st
        token = st.secrets["GITHUB_TOKEN"]
        repo  = st.secrets["GITHUB_REPO"]   # "username/repo-name"
        branch = st.secrets.get("GITHUB_BRANCH", "main")
        return token, repo, branch
    except Exception:
        return None, None, "main"

GH_API = "https://api.github.com"

# ── GitHub 파일 읽기 ──
def _gh_get(path, token, repo, branch):
    url = f"{GH_API}/repos/{repo}/contents/{path}?ref={branch}"
    r = requests.get(url, headers={"Authorization": f"token {token}"}, timeout=10)
    if r.status_code == 200:
        data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return json.loads(content), data["sha"]
    return None, None

# ── GitHub 파일 쓰기 ──
def _gh_put(path, content_str, token, repo, branch, sha=None):
    url = f"{GH_API}/repos/{repo}/contents/{path}"
    body = {
        "message": f"update {path}",
        "content": base64.b64encode(content_str.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        body["sha"] = sha
    r = requests.put(url, json=body,
                     headers={"Authorization": f"token {token}"}, timeout=15)
    return r.status_code in (200, 201)

# ── GitHub 이미지 업로드 ──
def gh_upload_image(filename, file_bytes, token, repo, branch):
    path = f"assets/paintings/{filename}"
    url = f"{GH_API}/repos/{repo}/contents/{path}"
    # 이미 있으면 sha 가져오기
    r = requests.get(url, headers={"Authorization": f"token {token}"}, timeout=10)
    sha = r.json().get("sha") if r.status_code == 200 else None
    body = {
        "message": f"upload {filename}",
        "content": base64.b64encode(file_bytes).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        body["sha"] = sha
    r = requests.put(url, json=body,
                     headers={"Authorization": f"token {token}"}, timeout=30)
    if r.status_code in (200, 201):
        # raw URL 반환
        raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
        return raw_url
    return None

# ── 로컬 fallback 경로 ──
DATA_DIR   = "data"
LOCAL_PAINTINGS = "data/paintings.json"
LOCAL_CONTACT   = "data/contact.json"
LOCAL_TEXTS     = "data/texts.json"

def _ensure_local():
    Path(DATA_DIR).mkdir(exist_ok=True)
    Path("assets/paintings").mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────
# paintings
# ────────────────────────────────────────────
def load_paintings():
    token, repo, branch = get_gh_config()
    if token and repo:
        data, _ = _gh_get("data/paintings.json", token, repo, branch)
        if data is not None:
            return data
    # 로컬 fallback
    _ensure_local()
    if os.path.exists(LOCAL_PAINTINGS):
        with open(LOCAL_PAINTINGS, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_paintings(paintings):
    token, repo, branch = get_gh_config()
    content = json.dumps(paintings, ensure_ascii=False, indent=2)
    if token and repo:
        _, sha = _gh_get("data/paintings.json", token, repo, branch)
        _gh_put("data/paintings.json", content, token, repo, branch, sha)
    # 로컬에도 저장 (로컬 실행 대비)
    _ensure_local()
    with open(LOCAL_PAINTINGS, "w", encoding="utf-8") as f:
        f.write(content)

# ────────────────────────────────────────────
# contact
# ────────────────────────────────────────────
DEFAULT_CONTACT = {
    "phone": "010-6665-3430",
    "instagram": "@gyungkyu3",
    "intro": "꽃과 풍경을 담은 원화를 판매합니다.\n구매 문의는 전화 또는 인스타그램 DM으로 연락 주세요."
}

def get_contact_info():
    token, repo, branch = get_gh_config()
    if token and repo:
        data, _ = _gh_get("data/contact.json", token, repo, branch)
        if data:
            return {**DEFAULT_CONTACT, **data}
    _ensure_local()
    if os.path.exists(LOCAL_CONTACT):
        with open(LOCAL_CONTACT, encoding="utf-8") as f:
            return {**DEFAULT_CONTACT, **json.load(f)}
    return DEFAULT_CONTACT

def save_contact_info(info):
    token, repo, branch = get_gh_config()
    content = json.dumps(info, ensure_ascii=False, indent=2)
    if token and repo:
        _, sha = _gh_get("data/contact.json", token, repo, branch)
        _gh_put("data/contact.json", content, token, repo, branch, sha)
    _ensure_local()
    with open(LOCAL_CONTACT, "w", encoding="utf-8") as f:
        f.write(content)

# ────────────────────────────────────────────
# site texts
# ────────────────────────────────────────────
DEFAULT_TEXTS = {
    "site_title": "Atelier",
    "site_subtitle": "꽃과 풍경, 그리고 따뜻한 시간",
    "site_tagline": "Original Paintings · Handmade with Love",
    "intro_line1": "일상에 꽃 한 송이, 풍경 한 폭을 들이세요.",
    "intro_line2": "모든 작품은 직접 그린 원화입니다.",
    "cta_title": "마음에 드는 작품이 있으신가요?",
    "cta_sub": "구매 문의는 아래 연락처로 편하게 연락 주세요",
    "footer_text": "© 2025 Atelier · All artworks are original and handmade · 무단 복제 및 배포 금지",
}

def get_site_texts():
    token, repo, branch = get_gh_config()
    if token and repo:
        data, _ = _gh_get("data/texts.json", token, repo, branch)
        if data:
            return {**DEFAULT_TEXTS, **data}
    _ensure_local()
    if os.path.exists(LOCAL_TEXTS):
        with open(LOCAL_TEXTS, encoding="utf-8") as f:
            return {**DEFAULT_TEXTS, **json.load(f)}
    return DEFAULT_TEXTS

def save_site_texts(texts):
    token, repo, branch = get_gh_config()
    content = json.dumps(texts, ensure_ascii=False, indent=2)
    if token and repo:
        _, sha = _gh_get("data/texts.json", token, repo, branch)
        _gh_put("data/texts.json", content, token, repo, branch, sha)
    _ensure_local()
    with open(LOCAL_TEXTS, "w", encoding="utf-8") as f:
        f.write(content)

def get_categories(paintings):
    cats = set(p["category"] for p in paintings if p.get("category"))
    return sorted(list(cats))
