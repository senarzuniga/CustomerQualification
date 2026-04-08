import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.session_manager import SessionManager

SessionManager.init_session()

st.set_page_config(page_title="Informes y Exportacion", page_icon="📄", layout="wide")

st.title("📄 Informes y Exportacion")
st.markdown("*Genera y descarga informes profesionales en PDF y Excel*")
st.markdown("---")

try:
    from utils.database import CompanyDatabase
    db = CompanyDatabase()
    companies = db.get_all_companies()
except Exception as e:
    st.error(f"Error conectando a base de datos: {e}")
    companies = []

if not companies:
    st.info("📭 No hay empresas guardadas. Ve a 'Analisis de Empresa' para analizar y guardar una empresa.")
    st.stop()

company_options = {f"{c['name']} (ID:{c['id']})": c["id"] for c in companies}

default_idx = 0
if "dashboard_selected_company_id" in st.session_state:
    target_id = st.session_state["dashboard_selected_company_id"]
    for i, (label, cid) in enumerate(company_options.items()):
        if cid == target_id:
            default_idx = i
            break

selected = st.selectbox("Selecciona empresa", list(company_options.keys()), index=default_idx)
cid = company_options[selected]

company_info = db.get_company(cid)
st.markdown(f"**{company_info['name']}** | Sector: {company_info.get('sector', 'N/D')} | Pais: {company_info.get('country', 'N/D')}")
st.markdown("---")

all_analysis = {"company_name": company_info["name"]}
for atype in ["enrichment", "financial", "market", "competitive", "strategic", "valuation", "report"]:
    data = db.get_latest_analysis(cid, atype)
    if data:
        all_analysis[atype] = data

report_data = all_analysis.get("report", {})
report_text = report_data.get("report_text", "")
executive_summary = report_data.get("executive_summary", "")

if executive_summary:
    with st.expander("📋 Resumen Ejecutivo", expanded=True):
        st.markdown(executive_summary)

if report_text:
    with st.expander("📄 Ver Informe Completo"):
        st.markdown(report_text)

st.markdown("---")
st.subheader("📥 Descargar Informes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 PDF")
    st.markdown("Informe completo con portada, secciones y formato profesional")
    if st.button("🔄 Generar PDF", type="primary", use_container_width=True):
        with st.spinner("Generando PDF..."):
            try:
                from utils.pdf_generator import PDFReportGenerator
                gen = PDFReportGenerator()
                pdf_bytes = gen.generate_report(company_info["name"], all_analysis, report_text or f"Informe: {company_info['name']}")
                st.session_state["pdf_bytes"] = pdf_bytes
                st.session_state["pdf_company"] = company_info["name"]
                st.success("✅ PDF generado")
            except Exception as e:
                st.error(f"Error generando PDF: {e}")

    if st.session_state.get("pdf_bytes") and st.session_state.get("pdf_company") == company_info["name"]:
        st.download_button(
            label="⬇️ Descargar PDF",
            data=st.session_state["pdf_bytes"],
            file_name=f"informe_{company_info['name'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

with col2:
    st.markdown("### 📊 Excel")
    st.markdown("6 hojas: Overview, Financial, SWOT, Valuation, Competitors, Scenarios")
    if st.button("🔄 Generar Excel", type="primary", use_container_width=True):
        with st.spinner("Generando Excel..."):
            try:
                from utils.excel_generator import ExcelReportGenerator
                gen = ExcelReportGenerator()
                excel_bytes = gen.generate_report(company_info["name"], all_analysis)
                st.session_state["excel_bytes"] = excel_bytes
                st.session_state["excel_company"] = company_info["name"]
                st.success("✅ Excel generado")
            except Exception as e:
                st.error(f"Error generando Excel: {e}")

    if st.session_state.get("excel_bytes") and st.session_state.get("excel_company") == company_info["name"]:
        st.download_button(
            label="⬇️ Descargar Excel",
            data=st.session_state["excel_bytes"],
            file_name=f"informe_{company_info['name'].replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
