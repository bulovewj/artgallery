import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils import get_contact_info

def show_contact():
    contact = get_contact_info()

    st.markdown("""
    <div class="section-title">— 연락하기 —</div>
    <div class="section-divider"></div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        intro = contact.get("intro", "").replace("\\n", "\n")

        # 상단 인트로
        st.markdown(f"""
        <div style="background:#F5F0E8;border:1px solid #D4C5B0;padding:40px;text-align:center;margin-bottom:24px;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:300;
                font-style:italic;color:#2C1810;margin-bottom:16px;">
                언제든 편히 연락 주세요
            </div>
            <div style="font-size:0.88rem;color:#8B6F5E;line-height:1.8;margin-bottom:30px;">
                {intro.replace(chr(10), "<br>")}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 연락처 — Streamlit 컴포넌트로
        phone     = contact.get("phone", "")
        instagram = contact.get("instagram", "")

        left, right = st.columns(2)
        with left:
            st.markdown(f"""
            <div style="text-align:center;padding:24px;border:1px solid #D4C5B0;background:white;">
                <div style="font-size:0.72rem;letter-spacing:0.2em;color:#7A8C6E;
                    text-transform:uppercase;margin-bottom:10px;">
                    📞 &nbsp;전화 / 문자
                </div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#2C1810;">
                    {phone}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with right:
            st.markdown(f"""
            <div style="text-align:center;padding:24px;border:1px solid #D4C5B0;background:white;">
                <div style="font-size:0.72rem;letter-spacing:0.2em;color:#7A8C6E;
                    text-transform:uppercase;margin-bottom:10px;">
                    📷 &nbsp;인스타그램
                </div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#2C1810;">
                    {instagram}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 구매 안내
        st.markdown("""
        <div style="border:1px solid #D4C5B0;padding:30px;background:#FAF7F2;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:300;
                font-style:italic;color:#2C1810;margin-bottom:20px;text-align:center;">
                구매 안내
            </div>
            <div style="font-size:0.85rem;color:#8B6F5E;line-height:2.2;letter-spacing:0.05em;">
                ✦ &nbsp;모든 작품은 직접 그린 원화입니다<br>
                ✦ &nbsp;작품 구매는 전화 또는 인스타그램 DM으로 문의해 주세요<br>
                ✦ &nbsp;포장 및 배송 방법은 개별 상담을 통해 안내드립니다<br>
                ✦ &nbsp;작품은 선착순으로 판매되며, 판매 완료 시 품절 처리됩니다<br>
                ✦ &nbsp;그림 주문 제작 문의도 환영합니다
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("← 갤러리로 돌아가기", key="back_to_gallery", use_container_width=True):
            st.session_state.page = 'gallery'
            st.rerun()
