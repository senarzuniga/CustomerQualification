import streamlit as st
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Customer Qualification Agent",
    page_icon="📊",
    layout="wide"
)

st.title("🎯 Customer Qualification Agent")
st.markdown("*Análisis profesional de datos de leads, contactos y empresas*")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📤 Status", "Listo")
with col2:
    st.metric("🔧 Versión", "1.0.0")
with col3:
    st.metric("✅ APIs", "12+")

st.success("✅ ¡Aplicación lista para usar!")
