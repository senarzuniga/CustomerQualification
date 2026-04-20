import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.session_manager import SessionManager

# INICIALIZAR SESIÓN AL INICIO
SessionManager.init_session()

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
    
    # Mostrar estado de datos
    st.markdown("### 📊 Estado de Sesión")
    if SessionManager.has_data():
        data = SessionManager.get_uploaded_data()
        st.success(f"✅ Datos cargados: {len(data)} registros")
        st.metric("Columnas", len(data.columns))
        if len(st.session_state.file_names) > 0:
            st.write("**Archivos:**")
            for fname in st.session_state.file_names:
                st.write(f"• {fname}")
    else:
        st.warning("⚠️ Sin datos cargados")
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuración")
    st.session_state.api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key)

# Main content
st.title("🎯 Customer Qualification Agent")
st.markdown("*Análisis profesional de datos de leads, contactos y empresas*")
st.markdown("---")

# Info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📤 Status", "✅ Listo")
with col2:
    st.metric("🔧 Versión", "1.0.0")
with col3:
    st.metric("✅ APIs", "12+")

st.info("ℹ️ Usa el menu lateral para navegar entre las diferentes funcionalidades")

st.markdown("""
## 🏢 Plataforma de Inteligencia Empresarial

### Sistema Multi-Agente de Analisis Estrategico
| Modulo | Descripcion |
|--------|-------------|
| 🏢 **Analisis de Empresa** | Analisis completo con 7 agentes de IA |
| 📊 **Dashboard Empresas** | Vista consolidada de empresas analizadas |
| 📄 **Informes** | Exportacion PDF y Excel profesional |

### Flujo de Analisis Estrategico
1. **Analisis de Empresa** → Introduce el nombre y ejecuta el analisis completo
2. **7 Agentes IA** → Enriquecimiento, Financiero, Mercado, Competitivo, Estrategico, Valoracion, Informe
3. **Dashboard** → Consulta y compara empresas analizadas
4. **Exportacion** → Descarga informes PDF y Excel de nivel consultoria

---

## 📋 Modulo Customer Qualification (Legacy)

- ✅ **Carga Multiformato**: Excel, CSV, PDF
- ✅ **Procesamiento Inteligente**: Limpieza y validacion automatica
- ✅ **Enriquecimiento IA**: OpenAI GPT-4
- ✅ **Dashboard Profesional**: KPIs y graficos
- ✅ **Exportacion**: Excel, CSV, PDF

---

**Version**: 2.0.0 | **Autor**: Senior Arzuniga
""")
