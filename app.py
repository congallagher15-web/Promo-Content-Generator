
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Promo Content Generator - MVP", page_icon="🎰", layout="centered")

st.image("assets/logo.png", width=280)
st.title("Promo Content Generator - MVP")
st.caption("Demo: upload ANY promo brief → receive promo content as a .docx.")

uploaded = st.file_uploader(
    "📎 Upload any promotion brief to demonstrate the flow (.docx, .doc, .pdf, .txt, .md, .html)",
    type=["docx", "doc", "pdf", "txt", "md", "html", "htm"],
    accept_multiple_files=False,
)

eng_path = Path("assets/22116_PSC_PragmaticDraw_ICE_V2.docx")
spa_path = Path("assets/22116_PSC_PragmaticDraw_ES_Structured.docx")
eng_bytes = eng_path.read_bytes()
spa_bytes = spa_path.read_bytes()

if uploaded is not None:
    st.success("✅ Brief received. Delivering brand-approved content (embedded).")
    st.download_button(
        label="⬇️ Download: Pragmatic Play Prize Draw (Approved, EN).docx",
        data=eng_bytes,
        file_name="Pragmatic_Play_Prize_Draw_Approved_EN.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("Translate")
    st.write("Only Spanish is available in this MVP.")
    if st.button("Translate → Spanish (ES)"):
        st.success("✅ Spanish version ready.")
        st.download_button(
            label="⬇️ Download: Sorteo de Premios Pragmatic (ES).docx",
            data=spa_bytes,
            file_name="Pragmatic_Play_Sorteo_de_Premios_ES.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
else:
    st.info("Drag & drop a file above to enable the download button.")
