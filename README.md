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

## 🛠️ Development Environment Setup

### Prerequisites

- Python 3.8+
- Git

### Setting Up the Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/senarzuniga/CustomerQualification.git
   cd CustomerQualification
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### IDE Configuration

- **Recommended IDE**: Visual Studio Code
- **Extensions**:
  - Python (for syntax highlighting and IntelliSense)
  - Pylint (for code linting)
  - GitLens (for Git integration)

### Common Issues

- Ensure that the virtual environment is activated before running any Python scripts.
- If you encounter issues with dependencies, try running `pip install --upgrade pip` before installing the requirements.

## 📝 Licencia

MIT License

---

**Versión**: 1.0.0  
**Autor**: Sénior Arzúniga
