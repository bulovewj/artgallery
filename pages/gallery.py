import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils import load_paintings, get_categories, get_site_texts

def show_gallery():
    paintings = load_paintings()
    texts     = get_site_texts()

    st.markdown(f"""
    <div class="intro-banner">
        <div class="intro-text">
            {texts.get("intro_line1","")}<br>
            {texts.get("intro_line2","")}
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

    categories = get_categories(paintings)
    all_cats   = ['전체'] + categories

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

    current_filter = st.session_state.get('filter', '전체')
    filtered = paintings if current_filter == '전체' else [p for p in paintings if p.get("category") == current_filter]

    if not filtered:
        st.markdown('<div class="empty-state"><div class="empty-state-text">해당 카테고리 작품이 없습니다</div></div>', unsafe_allow_html=True)
        return

    cols = st.columns(3, gap="medium")
    for idx, painting in enumerate(filtered):
        with cols[idx % 3]:
            is_sold = painting.get("sold", False)
            # image_url (GitHub raw) 또는 image_path (로컬) 둘 다 지원
            img_url = painting.get("image_url") or painting.get("image_path", "")

            if img_url:
                img_tag = f'<img src="{img_url}" alt="{painting.get("title","작품")}" style="width:100%;height:100%;object-fit:cover;">'
            else:
                img_tag = '<div style="width:100%;aspect-ratio:4/5;background:linear-gradient(135deg,#F5F0E8,#EDE5D8);display:flex;align-items:center;justify-content:center;color:#B8935A;font-size:2.5rem;">🎨</div>'

            sold_overlay = '<div class="sold-overlay"><div class="sold-badge">SOLD OUT</div></div>' if is_sold else ''
            new_badge    = '<div class="tag-new">New</div>' if painting.get("is_new") and not is_sold else ''
            price_class  = "painting-price sold" if is_sold else "painting-price"
            price_html   = f'<div class="{price_class}">{painting["price"]:,}원</div>' if painting.get("price") else ''
            size_html    = f' · {painting["size"]}' if painting.get("size") else ''
            desc_html    = f'<div style="font-size:0.78rem;color:#7A8C6E;margin-top:8px;line-height:1.6;">{painting["description"]}</div>' if painting.get("description") else ''

            st.markdown(f"""
            <div class="painting-card" style="margin-bottom:24px;">
                <div class="painting-img-container">
                    {img_tag}{sold_overlay}{new_badge}
                </div>
                <div class="painting-info">
                    <div class="painting-title">{painting.get("title","무제")}</div>
                    <div class="painting-meta">{painting.get("category","")}{size_html}</div>
                    {price_html}{desc_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown(f"""
        <div style="text-align:center;padding:30px;border:1px solid #D4C5B0;background:#FAF7F2;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:300;font-style:italic;color:#2C1810;margin-bottom:10px;">
                {texts.get("cta_title","")}
            </div>
            <div style="font-size:0.82rem;color:#8B6F5E;letter-spacing:0.08em;">
                {texts.get("cta_sub","")}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✉️  연락하기", key="go_contact", use_container_width=True):
            st.session_state.page = 'contact'
            st.rerun()
