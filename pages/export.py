import streamlit as st

st.set_page_config(page_title="Exportación", page_icon="💾")

st.title("💾 Exportación Profesional")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.button("📄 Generar Excel Leads")
with col2:
    st.button("🏢 Generar Excel Empresas")

st.info("ℹ️ Procesa datos primero")