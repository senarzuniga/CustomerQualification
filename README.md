# 🎯 Customer Qualification Agent

**Herramienta profesional de análisis de datos para calificación de leads, carteras de clientes y enriquecimiento de información empresarial.**

## 📋 Descripción

Customer Qualification Agent es una aplicación Streamlit diseñada para procesar, analizar y enriquecer datos de leads, contactos y empresas.

### Características Principales

✅ **Carga Multiformato**: Excel, CSV, PDF  
✅ **Procesamiento Inteligente**: Limpieza y validación automática  
✅ **Enriquecimiento de Datos**: 25+ campos de análisis empresarial  
✅ **Web Scraping Ético**: APIs públicas  
✅ **Análisis con IA**: OpenAI GPT-4  
✅ **Reportes Profesionales**: Excels formateados  

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/senarzuniga/CustomerQualification.git
cd CustomerQualification

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
streamlit run app.py
```

Abre tu navegador en [http://localhost:8501](http://localhost:8501)

## 📁 Estructura del Proyecto

```
CustomerQualification/
├── app.py                    # Aplicación principal
├── streamlit_app.py         # Para Streamlit Cloud
├── config.py                # Configuración
├── requirements.txt         # Dependencias
├── .env.example             # Variables de entorno
├── utils/                   # Módulos de lógica
│   ├── data_processor.py
│   ├── web_scraper.py
│   ├── ai_enrichment.py
│   ├── excel_generator.py
│   ├── analytics.py
│   ├── cache_manager.py
│   ├── ui_components.py
│   └── api_integrations.py
├── pages/                   # Páginas de la app
│   ├── dashboard.py
│   ├── data_upload.py
│   ├── processing.py
│   ├── enrichment.py
│   ├── analytics.py
│   ├── export.py
│   └── settings.py
├── .streamlit/
│   └── config.toml
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── streamlit_cloud_deploy.md
└── logs/
```

## 📊 Flujo de Trabajo

```
1. 📤 CARGA DE DATOS
   ↓
2. 🔍 PROCESAMIENTO
   ↓
3. ✨ ENRIQUECIMIENTO
   ↓
4. 📊 ANÁLISIS
   ↓
5. 💾 EXPORTACIÓN
```

## ☁️ Despliegue en Streamlit Cloud

Ver: [deployment/streamlit_cloud_deploy.md](deployment/streamlit_cloud_deploy.md)

## 🐳 Despliegue con Docker

```bash
docker-compose up --build
```

## 📚 Ejemplos de Uso

Aquí hay algunos ejemplos de cómo usar la aplicación para casos de uso comunes:

### Ejemplo 1: Procesamiento de un archivo CSV

```python
# Suponiendo que el entorno virtual está activado y las dependencias instaladas
import pandas as pd
from utils.data_processor import process_data

data = pd.read_csv('leads.csv')
processed_data = process_data(data)
print(processed_data.head())
```

### Ejemplo 2: Enriquecimiento de datos con IA

```python
from utils.ai_enrichment import enrich_data

enriched_data = enrich_data(processed_data)
print(enriched_data.head())
```

## 👨‍💻 Guía de Desarrollo

Para contribuir al proyecto, siga estas pautas:

- **Estilo de Código**: Use PEP 8 como guía para el estilo de código.
- **Pruebas**: Asegúrese de que todas las pruebas pasen antes de enviar un PR.
- **Commits**: Use mensajes de commit claros y descriptivos.
- **Revisiones**: Todas las contribuciones deben ser revisadas por al menos un mantenedor.

## 📝 Licencia

MIT License

---

**Versión**: 1.0.0  
**Autor**: Sénior Arzúniga
