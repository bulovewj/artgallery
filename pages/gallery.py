import streamlit as st
import base64
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils import load_paintings, get_categories

def img_to_base64(img_path):
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def show_gallery():
    paintings = load_paintings()

    # 인트로 배너
    st.markdown("""
    <div class="intro-banner">
        <div class="intro-text">
            일상에 꽃 한 송이, 풍경 한 폭을 들이세요.<br>
            모든 작품은 직접 그린 원화입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not paintings:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🎨</div>
            <div class="empty-state-text">아직 등록된 작품이 없습니다</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # 카테고리 필터
    categories = get_categories(paintings)
    all_cats = ['전체'] + categories

    st.markdown('<div class="section-title">— 작품 목록 —</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if len(all_cats) > 1:
        cols = st.columns(len(all_cats) + 2)
        for i, cat in enumerate(all_cats):
            with cols[i+1]:
                if st.button(cat, key=f"filter_{cat}"):
                    st.session_state.filter = cat
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

    # 필터 적용
    current_filter = st.session_state.get('filter', '전체')
    if current_filter == '전체':
        filtered = paintings
    else:
        filtered = [p for p in paintings if p.get("category") == current_filter]

    if not filtered:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-text">해당 카테고리 작품이 없습니다</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # 그리드 레이아웃 (3열)
    cols = st.columns(3, gap="medium")

    for idx, painting in enumerate(filtered):
        with cols[idx % 3]:
            is_sold = painting.get("sold", False)
            img_path = painting.get("image_path", "")
            b64 = img_to_base64(img_path) if img_path else None

            # 이미지 영역
            if b64:
                ext = Path(img_path).suffix.lower()
                mime = "image/jpeg" if ext in ['.jpg', '.jpeg'] else "image/png" if ext == '.png' else "image/webp"
                img_tag = f'<img src="data:{mime};base64,{b64}" alt="{painting.get("title","작품")}">'
            else:
                # 플레이스홀더
                img_tag = f'''
                <div style="width:100%;aspect-ratio:4/5;background:linear-gradient(135deg,#F5F0E8,#EDE5D8);
                    display:flex;align-items:center;justify-content:center;color:#B8935A;font-size:2.5rem;">
                    🎨
                </div>'''

            sold_overlay = ''
            if is_sold:
                sold_overlay = '<div class="sold-overlay"><div class="sold-badge">SOLD OUT</div></div>'

            new_badge = ''
            if painting.get("is_new", False) and not is_sold:
                new_badge = '<div class="tag-new">New</div>'

            price_html = ''
            if painting.get("price"):
                price_class = "painting-price sold" if is_sold else "painting-price"
                price_html = f'<div class="{price_class}">{painting["price"]:,}원</div>'

            size_html = ''
            if painting.get("size"):
                size_html = f' · {painting["size"]}'

            card_html = f"""
            <div class="painting-card" style="margin-bottom:24px;">
                <div class="painting-img-container">
                    {img_tag}
                    {sold_overlay}
                    {new_badge}
                </div>
                <div class="painting-info">
                    <div class="painting-title">{painting.get("title", "무제")}</div>
                    <div class="painting-meta">{painting.get("category","")}{size_html}</div>
                    {price_html}
                    {f'<div style="font-size:0.78rem;color:#7A8C6E;margin-top:8px;line-height:1.6;">{painting.get("description","")}</div>' if painting.get("description") else ""}
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

    # 하단 연락 안내
    st.markdown("<br><br>", unsafe_allow_html=True)
    contact_col1, contact_col2, contact_col3 = st.columns([1,2,1])
    with contact_col2:
        st.markdown("""
        <div style="text-align:center;padding:30px;border:1px solid #D4C5B0;background:#FAF7F2;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:300;
                font-style:italic;color:#2C1810;margin-bottom:10px;">
                마음에 드는 작품이 있으신가요?
            </div>
            <div style="font-size:0.82rem;color:#8B6F5E;letter-spacing:0.08em;">
                구매 문의는 아래 연락처로 편하게 연락 주세요
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✉️  연락하기", key="go_contact", use_container_width=True):
            st.session_state.page = 'contact'
            st.rerun()
