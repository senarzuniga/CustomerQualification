import streamlit as st
from utils.session_manager import SessionManager

st.set_page_config(page_title="Procesamiento", page_icon="🔄")

# Inicializar sesión
SessionManager.init_session()

st.title("🔄 Procesamiento de Datos")
st.markdown("---")

# Verificar si hay datos
if not SessionManager.has_data():
    st.warning("⚠️ No hay datos cargados")
    st.info("1. Ve a **Carga de Datos** (menú lateral)")
    st.info("2. Carga un archivo")
    st.info("3. Haz clic en **Procesar Datos**")
    st.info("4. Vuelve aquí para ver los resultados")
else:
    df = SessionManager.get_uploaded_data()
    
    st.success(f"✅ Datos disponibles: {len(df)} registros")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Registros", len(df))
    with col2:
        st.metric("📋 Columnas", len(df.columns))
    with col3:
        if len(df) > 0 and len(df.columns) > 0:
            null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        else:
            null_pct = 0
        st.metric("✅ Completitud", f"{100 - null_pct:.1f}%")
    
    st.markdown("---")
    st.subheader("📊 Vista Previa de Datos")
    st.dataframe(df.head(20), use_container_width=True)
    
    st.markdown("---")
    st.subheader("📈 Tipos de Datos")
    st.dataframe(df.dtypes.astype(str), use_container_width=True)
    
    st.markdown("---")
    st.subheader("📥 Descargar")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="datos_procesados.csv",
            mime="text/csv",
            use_container_width=True
        )
