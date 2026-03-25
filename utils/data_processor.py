import pandas as pd
import numpy as np
from PyPDF2 import PdfReader
import logging
from io import BytesIO
from typing import List, Optional

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

class DataProcessor:
    """Procesar y limpiar datos de archivos Excel, CSV y PDF"""
    
    def __init__(self):
        pass
    
    def process_files(self, uploaded_files: List) -> pd.DataFrame:
        """Procesar múltiples archivos y retornar DataFrame combinado"""
        all_data = []
        
        for file in uploaded_files:
            logger.info(f"Procesando archivo: {file.name}")
            
            try:
                # Leer según el tipo de archivo
                if file.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file)
                    logger.info(f"Archivo Excel leído: {file.name}")
                    
                elif file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                    logger.info(f"Archivo CSV leído: {file.name}")
                    
                elif file.name.endswith('.pdf'):
                    df = self._process_pdf(file)
                    if df is None:
                        logger.warning(f"No se pudieron extraer datos del PDF: {file.name}")
                        continue
                    logger.info(f"Archivo PDF leído: {file.name}")
                    
                else:
                    logger.warning(f"Archivo no soportado: {file.name}")
                    continue
                
                # Validar que el DataFrame no esté vacío
                if df is not None and not df.empty:
                    logger.info(f"DataFrame válido: {len(df)} filas, {len(df.columns)} columnas")
                    all_data.append(df)
                else:
                    logger.warning(f"DataFrame vacío para: {file.name}")
                    
            except Exception as e:
                logger.error(f"Error procesando {file.name}: {str(e)}")
                continue
        
        # Si no hay datos, retornar DataFrame vacío
        if not all_data:
            logger.warning("No se procesó ningún archivo correctamente")
            return pd.DataFrame()
        
        # Combinar todos los DataFrames
        combined_df = pd.concat(all_data, ignore_index=True)
        logger.info(f"DataFrames combinados: {len(combined_df)} filas totales")
        
        # Limpiar datos
        combined_df = self._clean_data(combined_df)
        
        return combined_df
    
    def _process_pdf(self, file) -> Optional[pd.DataFrame]:
        """Extraer texto/tablas de PDF"""
        try:
            reader = PdfReader(file)
            text = ""
            
            for page_num, page in enumerate(reader.pages):
                text += f"\n--- Página {page_num + 1} ---\n"
                text += page.extract_text()
            
            # Crear un simple DataFrame con el texto
            # En producción, usar librerías como tabula-py o pdfplumber
            if text.strip():
                df = pd.DataFrame({"contenido": [text]})
                return df
            
            logger.warning("No se extrajo texto del PDF")
            return None
            
        except Exception as e:
            logger.error(f"Error leyendo PDF: {str(e)}")
            return None
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar y validar datos"""
        logger.info("Iniciando limpieza de datos...")
        
        # Eliminar filas completamente vacías
        df = df.dropna(how='all')
        logger.info(f"Después de eliminar filas vacías: {len(df)} filas")
        
        # Eliminar duplicados
        df = df.drop_duplicates(keep='first')
        logger.info(f"Después de eliminar duplicados: {len(df)} filas")
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        logger.info(f"Columnas limpiadas: {list(df.columns)}")
        
        # Rellenar NaN con valores apropiados
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('')
            else:
                df[col] = df[col].fillna(0)
        
        logger.info("Limpieza completada")
        return df
