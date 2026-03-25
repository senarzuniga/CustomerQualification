import streamlit as st

st.set_page_config(page_title="Dashboard", page_icon="📈")

st.title("📈 Dashboard Ejecutivo")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Registros", 0)
with col2:
    st.metric("Leads", 0)
with col3:
    st.metric("Empresas", 0)
with col4:
    st.metric("Enriquecidos", "0%")

st.info("ℹ️ Carga datos para ver métricas")