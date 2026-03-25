import streamlit as st

st.set_page_config(page_title="Configuración", page_icon="⚙️")

st.title("⚙️ Configuración")
st.markdown("---")

st.subheader("APIs")
api_key = st.text_input("OpenAI API Key", type="password")

st.subheader("Preferencias")
st.checkbox("Tema oscuro")
st.slider("Nivel de logging", 0, 10, 5)