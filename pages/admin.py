import streamlit as st
import uuid
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils import load_paintings, save_paintings, get_contact_info, save_contact_info, get_site_texts, save_site_texts

ADMIN_PASSWORD = "200320"
UPLOAD_DIR = "assets/paintings"

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

    tab1, tab2, tab3, tab4 = st.tabs(["🖼️  작품 관리", "➕  작품 등록", "✏️  텍스트 편집", "📋  연락처 설정"])

    with tab1:
        _manage_paintings()
    with tab2:
        _add_painting()
    with tab3:
        _edit_texts()
    with tab4:
        _manage_contact()

def _show_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div style="border:1px solid #D4C5B0;padding:40px;background:#FAF7F2;text-align:center;margin-top:20px;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:300;
                font-style:italic;color:#2C1810;margin-bottom:24px;">
                관리자 로그인
            </div>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input("비밀번호", type="password", placeholder="관리자 비밀번호를 입력하세요")
        if st.button("로그인", use_container_width=True):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("✓ 로그인 되었습니다")
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다")

def _edit_texts():
    st.markdown("#### 사이트 텍스트 편집")
    st.caption("갤러리에 표시되는 글자들을 직접 수정할 수 있어요.")

    texts = get_site_texts()

    with st.form("texts_form"):
        st.markdown("**헤더 영역**")
        site_title = st.text_input("사이트 제목", value=texts.get("site_title", "Atelier"))
        site_subtitle = st.text_input("부제목 (이탤릭)", value=texts.get("site_subtitle", "꽃과 풍경, 그리고 따뜻한 시간"))
        site_tagline = st.text_input("태그라인", value=texts.get("site_tagline", "Original Paintings · Handmade with Love"))

        st.markdown("---")
        st.markdown("**갤러리 인트로 배너**")
        intro_line1 = st.text_input("첫째 줄", value=texts.get("intro_line1", "일상에 꽃 한 송이, 풍경 한 폭을 들이세요."))
        intro_line2 = st.text_input("둘째 줄", value=texts.get("intro_line2", "모든 작품은 직접 그린 원화입니다."))

        st.markdown("---")
        st.markdown("**갤러리 하단 문구**")
        cta_title = st.text_input("구매 유도 문구", value=texts.get("cta_title", "마음에 드는 작품이 있으신가요?"))
        cta_sub = st.text_input("구매 유도 설명", value=texts.get("cta_sub", "구매 문의는 아래 연락처로 편하게 연락 주세요"))

        st.markdown("---")
        st.markdown("**푸터**")
        footer_text = st.text_input("푸터 텍스트", value=texts.get("footer_text", "© 2025 Atelier · All artworks are original and handmade · 무단 복제 및 배포 금지"))

        if st.form_submit_button("✓  저장하기", use_container_width=True):
            save_site_texts({
                "site_title": site_title,
                "site_subtitle": site_subtitle,
                "site_tagline": site_tagline,
                "intro_line1": intro_line1,
                "intro_line2": intro_line2,
                "cta_title": cta_title,
                "cta_sub": cta_sub,
                "footer_text": footer_text,
            })
            st.success("✓ 텍스트가 저장되었습니다! 페이지를 새로고침하면 반영돼요.")

def _add_painting():
    st.markdown("#### 새 작품 등록")
    with st.form("add_painting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("작품 제목 *", placeholder="예: 봄날의 장미")
            category = st.selectbox("카테고리 *", ["꽃", "풍경", "정물", "추상", "기타"])
            price = st.number_input("가격 (원) *", min_value=0, step=1000, value=50000)
            size = st.text_input("크기", placeholder="예: A4, 20×30cm")
        with col2:
            description = st.text_area("작품 설명", placeholder="작품에 대한 간단한 설명", height=100)
            is_new = st.checkbox("NEW 배지 표시", value=True)
            uploaded_file = st.file_uploader("작품 이미지 *", type=["jpg", "jpeg", "png", "webp"])

        submitted = st.form_submit_button("✓  작품 등록하기", use_container_width=True)
        if submitted:
            if not title:
                st.error("작품 제목을 입력해주세요")
                return
            if not uploaded_file:
                st.error("작품 이미지를 업로드해주세요")
                return
            Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
            ext = Path(uploaded_file.name).suffix.lower()
            filename = f"{uuid.uuid4().hex}{ext}"
            img_path = os.path.join(UPLOAD_DIR, filename)
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            paintings = load_paintings()
            paintings.append({
                "id": str(uuid.uuid4()),
                "title": title, "category": category, "price": price,
                "size": size, "description": description,
                "image_path": img_path, "sold": False, "is_new": is_new
            })
            save_paintings(paintings)
            st.success(f"✓ '{title}' 작품이 등록되었습니다!")
            st.rerun()

def _manage_paintings():
    paintings = load_paintings()
    if not paintings:
        st.markdown('<div class="empty-state"><div class="empty-state-text">등록된 작품이 없습니다.</div></div>', unsafe_allow_html=True)
        return

    st.markdown(f"**총 {len(paintings)}개** · 판매중 {sum(1 for p in paintings if not p.get('sold'))}개 · 품절 {sum(1 for p in paintings if p.get('sold'))}개")
    st.markdown("---")

    for i, painting in enumerate(paintings):
        col1, col2, col3, col4 = st.columns([2, 3, 1.5, 1.5])
        with col1:
            img_path = painting.get("image_path", "")
            if img_path and os.path.exists(img_path):
                st.image(img_path, width=140)
            else:
                st.markdown("🖼️ 이미지 없음")
        with col2:
            status = "🔴 품절" if painting.get("sold") else "🟢 판매중"
            new_badge = " ✨NEW" if painting.get("is_new") else ""
            st.markdown(f"**{painting.get('title', '무제')}**{new_badge}")
            st.markdown(f"카테고리: {painting.get('category', '-')}")
            st.markdown(f"가격: **{painting.get('price', 0):,}원**")
            if painting.get('size'):
                st.markdown(f"크기: {painting.get('size')}")
            st.markdown(f"상태: {status}")
        with col3:
            if painting.get("sold"):
                if st.button("판매중으로 변경", key=f"unsold_{i}", use_container_width=True):
                    paintings[i]["sold"] = False
                    save_paintings(paintings)
                    st.rerun()
            else:
                if st.button("품절 처리", key=f"sold_{i}", use_container_width=True):
                    paintings[i]["sold"] = True
                    save_paintings(paintings)
                    st.rerun()
            if painting.get("is_new"):
                if st.button("NEW 제거", key=f"new_{i}", use_container_width=True):
                    paintings[i]["is_new"] = False
                    save_paintings(paintings)
                    st.rerun()
            else:
                if st.button("NEW 추가", key=f"new_add_{i}", use_container_width=True):
                    paintings[i]["is_new"] = True
                    save_paintings(paintings)
                    st.rerun()
        with col4:
            new_price = st.number_input("가격 수정", value=painting.get("price", 0), step=1000, key=f"price_{i}")
            if st.button("가격 저장", key=f"save_price_{i}", use_container_width=True):
                paintings[i]["price"] = new_price
                save_paintings(paintings)
                st.success("저장됨")
                st.rerun()
            if st.button("🗑️  삭제", key=f"delete_{i}", use_container_width=True):
                img_path = painting.get("image_path", "")
                if img_path and os.path.exists(img_path):
                    os.remove(img_path)
                paintings.pop(i)
                save_paintings(paintings)
                st.rerun()
        st.markdown("---")

def _manage_contact():
    st.markdown("#### 연락처 설정")
    contact = get_contact_info()
    with st.form("contact_form"):
        phone = st.text_input("전화번호", value=contact.get("phone", ""), placeholder="010-0000-0000")
        instagram = st.text_input("인스타그램 아이디", value=contact.get("instagram", ""), placeholder="@instagram_id")
        intro = st.text_area("소개 문구", value=contact.get("intro", ""), height=120)
        if st.form_submit_button("✓  저장하기", use_container_width=True):
            save_contact_info({"phone": phone, "instagram": instagram, "intro": intro})
            st.success("✓ 저장되었습니다!")

    st.markdown("---")
    if st.button("로그아웃"):
        st.session_state.admin_logged_in = False
        st.session_state.page = 'gallery'
        st.rerun()
