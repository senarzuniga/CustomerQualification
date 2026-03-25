import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="Customer Qualification Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'enriched_data' not in st.session_state:
    st.session_state.enriched_data = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

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
    st.markdown("### ⚙️ Configuración")
    st.session_state.api_key = st.text_input("OpenAI API Key", type="password", help="Opcional")
    
    st.markdown("---")
    st.markdown("### 📊 Estado")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cargados", "Sí" if st.session_state.uploaded_data is not None else "No")
    with col2:
        st.metric("Procesados", "Sí" if st.session_state.processed_data is not None else "No")

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

1. Ve a **Carga de Datos** en el menú lateral
2. Carga un archivo Excel, CSV o PDF
3. Procesa y valida automáticamente
4. Enriquece con datos de mercado
5. Exporta reportes profesionales
6. ¡Usa los insights para tomar decisiones!

---

**Versión**: 1.0.0 | **Autor**: Sénior Arzúniga
""")
