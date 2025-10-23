
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Promo Content Generator — MVP (Embedded)", page_icon="🎰", layout="centered")
st.title("🎰 Promo Content Generator — MVP (Embedded)")
st.caption("Management demo: upload ANY promo brief → receive the pre-approved, word-for-word content as a .docx.")

uploaded = st.file_uploader(
    "📎 Upload any promotion brief to demonstrate the flow (.docx, .doc, .pdf, .txt, .md, .html)",
    type=["docx", "doc", "pdf", "txt", "md", "html", "htm"],
    accept_multiple_files=False,
)

asset_path = Path(__file__).parent / "assets" / "22116_PSC_PragmaticDraw_ICE_V2.docx"
docx_bytes = asset_path.read_bytes()

if uploaded is not None:
    st.success("✅ Brief received. Delivering brand-approved content (embedded).")
    st.download_button(
        label="⬇️ Download: Pragmatic Play $20,000 Prize Draw (Approved).docx",
        data=docx_bytes,
        file_name="Pragmatic_Play_20000_Prize_Draw_Approved.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )
else:
    st.info("Drag & drop a file above to enable the download button.")
