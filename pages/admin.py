import streamlit as st
import uuid
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils import (load_paintings, save_paintings,
                   get_contact_info, save_contact_info,
                   get_site_texts, save_site_texts,
                   gh_upload_image, get_gh_config)

ADMIN_PASSWORD = "200320"

def show_admin():
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        _show_login()
        return

    st.markdown("""
    <div class="section-title">— 관리자 페이지 —</div>
    <div class="section-divider"></div>
    """, unsafe_allow_html=True)

    # GitHub 연결 상태 표시
    token, repo, branch = get_gh_config()
    if token and repo:
        st.success(f"✓ GitHub 연결됨 · `{repo}` ({branch})")
    else:
        st.warning("⚠️ GitHub 미연결 — Streamlit Secrets에 GITHUB_TOKEN, GITHUB_REPO를 설정하면 데이터가 영구 저장됩니다.")

    tab1, tab2, tab3, tab4 = st.tabs(["🖼️  작품 관리", "➕  작품 등록", "✏️  텍스트 편집", "📋  연락처 설정"])
    with tab1: _manage_paintings()
    with tab2: _add_painting()
    with tab3: _edit_texts()
    with tab4: _manage_contact()

def _show_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div style="border:1px solid #D4C5B0;padding:40px;background:#FAF7F2;text-align:center;margin-top:20px;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:300;
                font-style:italic;color:#2C1810;margin-bottom:24px;">관리자 로그인</div>
        </div>
        """, unsafe_allow_html=True)
        pw = st.text_input("비밀번호", type="password", placeholder="관리자 비밀번호를 입력하세요")
        if st.button("로그인", use_container_width=True):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다")

def _add_painting():
    st.markdown("#### 새 작품 등록")
    token, repo, branch = get_gh_config()

    with st.form("add_painting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title       = st.text_input("작품 제목 *", placeholder="예: 봄날의 장미")
            category    = st.selectbox("카테고리 *", ["꽃", "풍경", "정물", "추상", "기타"])
            price       = st.number_input("가격 (원) *", min_value=0, step=1000, value=50000)
            size        = st.text_input("크기", placeholder="예: A4, 20×30cm")
        with col2:
            description = st.text_area("작품 설명", placeholder="작품에 대한 간단한 설명", height=100)
            is_new      = st.checkbox("NEW 배지 표시", value=True)
            uploaded    = st.file_uploader("작품 이미지 *", type=["jpg","jpeg","png","webp"])

        submitted = st.form_submit_button("✓  작품 등록하기", use_container_width=True)

        if submitted:
            if not title:
                st.error("작품 제목을 입력해주세요"); return
            if not uploaded:
                st.error("작품 이미지를 업로드해주세요"); return

            ext      = Path(uploaded.name).suffix.lower()
            filename = f"{uuid.uuid4().hex}{ext}"
            file_bytes = uploaded.getvalue()

            # GitHub에 이미지 업로드
            if token and repo:
                with st.spinner("이미지를 GitHub에 저장하는 중..."):
                    img_url = gh_upload_image(filename, file_bytes, token, repo, branch)
                if not img_url:
                    st.error("이미지 업로드 실패. GitHub 설정을 확인해주세요."); return
            else:
                # 로컬 fallback
                Path("assets/paintings").mkdir(parents=True, exist_ok=True)
                local_path = f"assets/paintings/{filename}"
                with open(local_path, "wb") as f:
                    f.write(file_bytes)
                img_url = local_path

            paintings = load_paintings()
            paintings.append({
                "id": str(uuid.uuid4()),
                "title": title, "category": category, "price": price,
                "size": size, "description": description,
                "image_url": img_url,        # raw GitHub URL 저장
                "sold": False, "is_new": is_new
            })
            save_paintings(paintings)
            st.success(f"✓ '{title}' 작품이 등록되었습니다!")
            st.rerun()

def _manage_paintings():
    paintings = load_paintings()
    if not paintings:
        st.info("등록된 작품이 없습니다. '작품 등록' 탭에서 추가해주세요.")
        return

    st.markdown(f"**총 {len(paintings)}개** · 판매중 {sum(1 for p in paintings if not p.get('sold'))}개 · 품절 {sum(1 for p in paintings if p.get('sold'))}개")
    st.markdown("---")

    for i, p in enumerate(paintings):
        c1, c2, c3, c4 = st.columns([2, 3, 1.5, 1.5])
        with c1:
            url = p.get("image_url", p.get("image_path", ""))
            if url:
                st.image(url, width=140)
            else:
                st.markdown("🖼️ 이미지 없음")
        with c2:
            st.markdown(f"**{p.get('title','무제')}**{'  ✨NEW' if p.get('is_new') else ''}")
            st.markdown(f"카테고리: {p.get('category','-')}  |  {'🔴 품절' if p.get('sold') else '🟢 판매중'}")
            st.markdown(f"가격: **{p.get('price',0):,}원**" + (f"  |  {p.get('size')}" if p.get('size') else ""))
        with c3:
            if p.get("sold"):
                if st.button("판매중으로", key=f"unsold_{i}", use_container_width=True):
                    paintings[i]["sold"] = False; save_paintings(paintings); st.rerun()
            else:
                if st.button("품절 처리", key=f"sold_{i}", use_container_width=True):
                    paintings[i]["sold"] = True; save_paintings(paintings); st.rerun()
            if p.get("is_new"):
                if st.button("NEW 제거", key=f"rmnew_{i}", use_container_width=True):
                    paintings[i]["is_new"] = False; save_paintings(paintings); st.rerun()
            else:
                if st.button("NEW 추가", key=f"addnew_{i}", use_container_width=True):
                    paintings[i]["is_new"] = True; save_paintings(paintings); st.rerun()
        with c4:
            new_price = st.number_input("가격 수정", value=p.get("price",0), step=1000, key=f"price_{i}")
            if st.button("저장", key=f"savep_{i}", use_container_width=True):
                paintings[i]["price"] = new_price; save_paintings(paintings)
                st.success("저장됨"); st.rerun()
            if st.button("🗑️  삭제", key=f"del_{i}", use_container_width=True):
                paintings.pop(i); save_paintings(paintings); st.rerun()
        st.markdown("---")

def _edit_texts():
    st.markdown("#### 사이트 텍스트 편집")
    texts = get_site_texts()
    with st.form("texts_form"):
        st.markdown("**헤더**")
        site_title    = st.text_input("사이트 제목",   value=texts.get("site_title",""))
        site_subtitle = st.text_input("부제목 (이탤릭)", value=texts.get("site_subtitle",""))
        site_tagline  = st.text_input("태그라인",       value=texts.get("site_tagline",""))
        st.markdown("---")
        st.markdown("**갤러리 인트로 배너**")
        intro_line1 = st.text_input("첫째 줄", value=texts.get("intro_line1",""))
        intro_line2 = st.text_input("둘째 줄", value=texts.get("intro_line2",""))
        st.markdown("---")
        st.markdown("**갤러리 하단 문구**")
        cta_title = st.text_input("구매 유도 문구", value=texts.get("cta_title",""))
        cta_sub   = st.text_input("구매 유도 설명", value=texts.get("cta_sub",""))
        st.markdown("---")
        footer_text = st.text_input("푸터", value=texts.get("footer_text",""))
        if st.form_submit_button("✓  저장하기", use_container_width=True):
            save_site_texts({"site_title":site_title,"site_subtitle":site_subtitle,
                             "site_tagline":site_tagline,"intro_line1":intro_line1,
                             "intro_line2":intro_line2,"cta_title":cta_title,
                             "cta_sub":cta_sub,"footer_text":footer_text})
            st.success("✓ 저장되었습니다!")

def _manage_contact():
    st.markdown("#### 연락처 설정")
    contact = get_contact_info()
    with st.form("contact_form"):
        phone     = st.text_input("전화번호",        value=contact.get("phone",""))
        instagram = st.text_input("인스타그램 아이디", value=contact.get("instagram",""))
        intro     = st.text_area("소개 문구",         value=contact.get("intro",""), height=120)
        if st.form_submit_button("✓  저장하기", use_container_width=True):
            save_contact_info({"phone":phone,"instagram":instagram,"intro":intro})
            st.success("✓ 저장되었습니다!")
    st.markdown("---")
    if st.button("로그아웃"):
        st.session_state.admin_logged_in = False
        st.session_state.page = 'gallery'
        st.rerun()
