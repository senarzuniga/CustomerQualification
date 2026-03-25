import streamlit as st
import pandas as pd

class SessionManager:
    """Gestor centralizado de sesión para persistencia de datos"""
    
    @staticmethod
    def init_session():
        """Inicializar todas las variables de sesión"""
        if 'uploaded_data' not in st.session_state:
            st.session_state.uploaded_data = None
        if 'processed_data' not in st.session_state:
            st.session_state.processed_data = None
        if 'enriched_data' not in st.session_state:
            st.session_state.enriched_data = None
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""
        if 'file_names' not in st.session_state:
            st.session_state.file_names = []
    
    @staticmethod
    def set_uploaded_data(data):
        """Guardar datos cargados"""
        st.session_state.uploaded_data = data
        st.session_state.processed_data = data
    
    @staticmethod
    def get_uploaded_data():
        """Obtener datos cargados"""
        return st.session_state.uploaded_data
    
    @staticmethod
    def has_data():
        """Verificar si hay datos"""
        return st.session_state.uploaded_data is not None and not st.session_state.uploaded_data.empty
    
    @staticmethod
    def set_file_names(files):
        """Guardar nombres de archivos"""
        st.session_state.file_names = [f.name for f in files]
