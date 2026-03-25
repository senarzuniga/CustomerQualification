import streamlit as st
import pandas as pd
from utils.data_processor import DataProcessor
from utils.session_manager import SessionManager
import traceback

st.set_page_config(page_title="Carga de Datos", page_icon="📤")

# Inicializar sesión
SessionManager.init_session()

st.title("📤 Carga de Datos")
st.markdown("Sube archivos Excel, CSV o PDF con información de leads, contactos o empresas")
st.markdown("---")

# File uploader
uploaded_files = st.file_uploader(
    "Selecciona archivos (Excel, CSV o PDF)",
    type=["xlsx", "xls", "pdf", "csv"],
    accept_multiple_files=True,
    key="file_uploader_unique"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} archivo(s) cargado(s)")
    
    # Mostrar archivos cargados
    st.subheader("📁 Archivos cargados:")
    for i, file in enumerate(uploaded_files, 1):
        st.write(f"{i}. **{file.name}** - {file.size / 1024:.1f} KB")
    
    # Guardar nombres de archivos
    SessionManager.set_file_names(uploaded_files)
    
    # Botón de procesamiento
    if st.button("🔄 Procesar Datos Ahora", use_container_width=True, key="process_button"):
        with st.spinner("⏳ Procesando archivos..."):
            try:
                processor = DataProcessor()
                processed_data = processor.process_files(uploaded_files)
                
                if not processed_data.empty:
                    # GUARDAR EN SESSION STATE
                    SessionManager.set_uploaded_data(processed_data)
                    
                    st.success(f"✅ ¡{len(processed_data)} registros procesados correctamente!")
                    st.balloons()
                    
                    # Mostrar preview
                    st.subheader("📊 Preview de datos procesados:")
                    st.dataframe(processed_data.head(10), use_container_width=True)
                    
                    # Estadísticas
                    st.subheader("📈 Estadísticas:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Registros", len(processed_data))
                    with col2:
                        st.metric("Columnas", len(processed_data.columns))
                    with col3:
                        if len(processed_data) > 0 and len(processed_data.columns) > 0:
                            null_pct = (processed_data.isnull().sum().sum() / (len(processed_data) * len(processed_data.columns)) * 100)
                        else:
                            null_pct = 0
                        st.metric("Datos Válidos", f"{100 - null_pct:.1f}%")
                    
                    st.info("✅ Los datos están guardados en sesión. Ve a 'Procesamiento' para verlos.")
                else:
                    st.error("❌ No se pudieron procesar los datos - DataFrame vacío")
                    
            except Exception as e:
                st.error(f"❌ Error procesando datos")
                with st.expander("📋 Ver detalles del error"):
                    st.code(f"{type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}")
else:
    st.info("📌 Carga archivos Excel, CSV o PDF para comenzar")
