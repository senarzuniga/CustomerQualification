import streamlit as st
import pandas as pd

st.set_page_config(page_title="Carga de Datos", page_icon="📤")

st.title("📤 Carga de Datos")
st.markdown("---")

uploaded_files = st.file_uploader(
    "Selecciona archivos",
    type=["xlsx", "xls", "pdf", "csv"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} archivo(s) cargado(s)")
    for file in uploaded_files:
        st.write(f"📄 {file.name}")