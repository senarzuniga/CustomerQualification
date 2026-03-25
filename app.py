import streamlit as st
import os
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="Customer Qualification Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stTitle { color: #1F77B4; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎯 Customer Qualification")
    st.markdown("---")
    st.markdown("### Configuración")
    api_key = st.text_input("OpenAI API Key", type="password", help="Opcional")
    
# Main content
st.title("🎯 Customer Qualification Agent")
st.markdown("*Análisis profesional de datos de leads, contactos y empresas*")
st.markdown("---")

# Info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📤 Status", "Listo")
with col2:
    st.metric("🔧 Versión", "1.0.0")
with col3:
    st.metric("✅ APIs", "12+")

st.info("ℹ️ Usa el menú lateral para navegar entre las diferentes funcionalidades")

st.markdown("""
## 📋 Características Principales

- ✅ **Carga Multiformato**: Excel, CSV, PDF
- ✅ **Procesamiento Inteligente**: Limpieza y validación automática
- ✅ **Web Scraping Ético**: APIs públicas
- ✅ **Enriquecimiento IA**: OpenAI GPT-4
- ✅ **Dashboard Profesional**: KPIs y gráficos
- ✅ **Exportación**: Excel, CSV, PDF

## 🚀 Inicio Rápido

1. Carga tus datos (Excel, CSV o PDF)
2. Procesa y valida automáticamente
3. Enriquece con datos de mercado
4. Exporta reportes profesionales
5. ¡Usa los insights para tomar decisiones!
""")
