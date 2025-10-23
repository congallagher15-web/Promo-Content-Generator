
import json
import streamlit as st
from src.parser import parse_brief
from src.generator import generate_content_docx, generate_markdown_preview

st.set_page_config(page_title="Promo Content Generator (MVP)", page_icon="🎰", layout="wide")
st.title("🎰 Promo Content Generator — MVP")
st.caption("Upload a promo brief → auto-generate brand-formatted content → download a Word doc. Offline, no API required.")

uploaded = st.file_uploader(
    "📎 Upload a promotion brief (.docx, .doc, .html, .txt, .md, .pdf)",
    type=["docx", "doc", "html", "htm", "txt", "md", "pdf"],
    accept_multiple_files=False,
)

if uploaded:
    st.info(f"Processing: **{uploaded.name}**")
    try:
        brief_bytes = uploaded.read()
        parsed = parse_brief(brief_bytes, uploaded.name)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.subheader("🧾 Parsed key facts (auto)")
    st.json(parsed, expanded=False)

    st.subheader("Preview")
    md = generate_markdown_preview(parsed)
    st.markdown(md)

    # Build and offer .docx
    docx_bytes = generate_content_docx(parsed)
    st.download_button(
        "⬇️ Download Promotion Content (.docx)",
        data=docx_bytes,
        file_name="promotion_content.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )
else:
    st.info("Drag and drop a promo brief above to begin.")
