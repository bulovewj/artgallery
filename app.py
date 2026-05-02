import streamlit as st
from utils import load_paintings, get_contact_info

st.set_page_config(
    page_title="Atelier — 원진 갤러리",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Noto+Serif+KR:wght@300;400;600&display=swap');
:root {
    --cream: #F5F0E8; --warm-white: #FAF7F2; --espresso: #2C1810;
    --latte: #8B6F5E; --sage: #7A8C6E; --gold: #B8935A; --border: #D4C5B0;
}
html, body, [class*="css"] { font-family: 'Noto Serif KR', serif; background-color: var(--warm-white); color: var(--espresso); }
.stApp { background-color: var(--warm-white); }
.gallery-header { text-align: center; padding: 60px 20px 40px; border-bottom: 1px solid var(--border); margin-bottom: 50px; }
.gallery-header::before { content: ''; display: block; width: 60px; height: 1px; background: var(--gold); margin: 0 auto 20px; }
.gallery-title { font-family: 'Cormorant Garamond', serif; font-size: 3.2rem; font-weight: 300; letter-spacing: 0.15em; color: var(--espresso); margin: 0; }
.gallery-subtitle { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; font-weight: 300; font-style: italic; color: var(--latte); margin-top: 8px; letter-spacing: 0.08em; }
.gallery-tagline { font-size: 0.85rem; color: var(--latte); margin-top: 16px; letter-spacing: 0.12em; font-weight: 300; }
.painting-card { background: white; border: 1px solid var(--border); overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease; position: relative; }
.painting-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(44,24,16,0.12); }
.painting-img-container { position: relative; overflow: hidden; aspect-ratio: 4/5; background: var(--cream); }
.painting-img-container img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.painting-card:hover .painting-img-container img { transform: scale(1.03); }
.sold-overlay { position: absolute; top:0; left:0; right:0; bottom:0; background: rgba(44,24,16,0.55); display:flex; align-items:center; justify-content:center; }
.sold-badge { color: white; font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 600; letter-spacing: 0.25em; border: 1px solid rgba(255,255,255,0.6); padding: 8px 20px; font-style: italic; }
.painting-info { padding: 18px 20px 20px; border-top: 1px solid var(--border); }
.painting-title { font-family: 'Cormorant Garamond', serif; font-size: 1.15rem; font-weight: 400; color: var(--espresso); margin: 0 0 4px; }
.painting-meta { font-size: 0.78rem; color: var(--latte); letter-spacing: 0.08em; font-weight: 300; }
.painting-price { font-family: 'Cormorant Garamond', serif; font-size: 1.05rem; color: var(--gold); font-weight: 400; margin-top: 10px; }
.painting-price.sold { color: var(--latte); text-decoration: line-through; font-size: 0.9rem; }
.contact-section { background: var(--cream); border: 1px solid var(--border); padding: 50px; text-align: center; margin: 60px 0; }
.contact-title { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 300; color: var(--espresso); margin-bottom: 12px; letter-spacing: 0.1em; font-style: italic; }
.contact-desc { font-size: 0.88rem; color: var(--latte); margin-bottom: 30px; line-height: 1.8; letter-spacing: 0.05em; }
.contact-items { display: flex; justify-content: center; gap: 50px; flex-wrap: wrap; }
.contact-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.contact-label { font-size: 0.72rem; letter-spacing: 0.2em; color: var(--sage); text-transform: uppercase; font-weight: 400; }
.contact-value { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: var(--espresso); font-weight: 400; }
.section-title { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 300; color: var(--espresso); text-align: center; margin: 40px 0 30px; letter-spacing: 0.12em; font-style: italic; }
.section-divider { width: 40px; height: 1px; background: var(--gold); margin: 0 auto 40px; }
.stButton > button { font-family: 'Noto Serif KR', serif !important; font-size: 0.8rem !important; letter-spacing: 0.12em !important; background: transparent !important; border: 1px solid var(--border) !important; color: var(--latte) !important; border-radius: 0 !important; padding: 8px 20px !important; transition: all 0.3s !important; }
.stButton > button:hover { background: var(--espresso) !important; color: white !important; border-color: var(--espresso) !important; }
.gallery-footer { text-align: center; padding: 30px; border-top: 1px solid var(--border); margin-top: 60px; font-size: 0.75rem; color: var(--latte); letter-spacing: 0.1em; }
.empty-state { text-align: center; padding: 80px 20px; color: var(--latte); }
.empty-state-text { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; font-weight: 300; font-style: italic; }
.intro-banner { background: linear-gradient(135deg, var(--cream) 0%, #EDE5D8 100%); border: 1px solid var(--border); padding: 40px; margin-bottom: 50px; text-align: center; }
.intro-text { font-family: 'Cormorant Garamond', serif; font-size: 1.05rem; font-weight: 300; font-style: italic; color: var(--latte); line-height: 2; letter-spacing: 0.05em; }
.tag-new { position: absolute; top: 14px; left: 14px; background: var(--sage); color: white; font-size: 0.65rem; letter-spacing: 0.15em; padding: 4px 10px; text-transform: uppercase; }
@media (max-width: 768px) { .gallery-title { font-size: 2.2rem; } .contact-items { gap: 30px; } .contact-section { padding: 30px 20px; } }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.block-container { padding-top: 0 !important; max-width: 1200px !important; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'gallery'
if 'filter' not in st.session_state:
    st.session_state.filter = '전체'

# 오른쪽 상단 관리자 버튼
top_left, top_right = st.columns([11, 1])
with top_right:
    is_logged = st.session_state.get('admin_logged_in', False)
    btn_label = "🔓" if is_logged else "🔒"
    if st.button(btn_label, key="admin_corner_btn", help="관리자"):
        st.session_state.page = 'admin'
        st.rerun()

# 헤더
st.markdown("""
<div class="gallery-header">
    <div class="gallery-title">Atelier</div>
    <div class="gallery-subtitle">꽃과 풍경, 그리고 따뜻한 시간</div>
    <div class="gallery-tagline">Original Paintings · Handmade with Love</div>
</div>
""", unsafe_allow_html=True)

# 네비게이션 (갤러리 + 연락하기)
col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])
with col2:
    if st.button("🎨  갤러리", key="nav_gallery", use_container_width=True):
        st.session_state.page = 'gallery'
        st.rerun()
with col3:
    if st.button("✉️  연락하기", key="nav_contact", use_container_width=True):
        st.session_state.page = 'contact'
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.page == 'gallery':
    from pages.gallery import show_gallery
    show_gallery()
elif st.session_state.page == 'contact':
    from pages.contact import show_contact
    show_contact()
elif st.session_state.page == 'admin':
    from pages.admin import show_admin
    show_admin()

st.markdown("""
<div class="gallery-footer">
    © 2025 Atelier · All artworks are original and handmade · 무단 복제 및 배포 금지
</div>
""", unsafe_allow_html=True)
