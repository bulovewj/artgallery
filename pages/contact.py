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

        st.markdown(f"""
        <div class="contact-section">
            <div class="contact-title">언제든 편히 연락 주세요</div>
            <div class="contact-desc">{intro.replace(chr(10), "<br>")}</div>
            <div class="contact-items">
                <div class="contact-item">
                    <div class="contact-label">📞&nbsp; 전화 / 문자</div>
                    <div class="contact-value">{contact.get("phone", "")}</div>
                </div>
                <div class="contact-item">
                    <div class="contact-label">📷&nbsp; 인스타그램</div>
                    <div class="contact-value">{contact.get("instagram", "")}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

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
