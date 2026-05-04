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

### Guía de Configuración Paso a Paso

1. **Clonar el Repositorio**: Asegúrate de tener Git instalado. Usa el comando `git clone` para obtener el código fuente.
2. **Crear y Activar Entorno Virtual**: Esto asegura que las dependencias no interfieran con otros proyectos.
3. **Instalar Dependencias**: Usa `pip install -r requirements.txt` para instalar todas las bibliotecas necesarias.
4. **Ejecutar la Aplicación**: Usa `streamlit run app.py` para iniciar la aplicación.

### Capturas de Pantalla

![Clonar Repositorio](images/clone_repo.png)
![Crear Entorno Virtual](images/create_venv.png)
![Instalar Dependencias](images/install_dependencies.png)
![Ejecutar Aplicación](images/run_app.png)

### Solución de Problemas Comunes

- **Error al activar el entorno virtual**: Asegúrate de que estás usando el comando correcto para tu sistema operativo.
- **Problemas de instalación de dependencias**: Verifica que `pip` esté actualizado.
- **La aplicación no se ejecuta**: Asegúrate de que `streamlit` esté instalado correctamente.

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

## 📝 Licencia

MIT License

---

**Versión**: 1.0.0  
**Autor**: Sénior Arzúniga
