import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.session_manager import SessionManager

SessionManager.init_session()

st.set_page_config(page_title="Dashboard Empresas", page_icon="📊", layout="wide")

st.title("📊 Dashboard de Empresas Analizadas")
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

# Metrics
total = len(companies)
col1, col2, col3 = st.columns(3)
col1.metric("🏢 Total Empresas", total)

vals = []
sale_probs = {"Alta": 0, "Media": 0, "Baja": 0}
for c in companies:
    try:
        val_data = db.get_latest_analysis(c["id"], "valuation")
        if val_data:
            v = val_data.get("valuation", {}).get("estimated_value_m")
            if v:
                vals.append(float(v))
            sp = val_data.get("sale_propensity", {}).get("probability", "")
            if sp in sale_probs:
                sale_probs[sp] += 1
    except Exception:
        pass

col2.metric("💎 Valoracion Media (M EUR)", f"{sum(vals)/len(vals):.1f}" if vals else "N/D")
col3.metric("🚨 Alta Propension Venta", sale_probs.get("Alta", 0))

st.markdown("---")

# Search
search = st.text_input("🔍 Buscar empresa", placeholder="Nombre o sector...")

# Table
import pandas as pd

display_companies = companies
if search:
    search_lower = search.lower()
    display_companies = [c for c in companies if search_lower in c["name"].lower() or search_lower in c.get("sector", "").lower()]

if not display_companies:
    st.warning("No se encontraron empresas con ese criterio de busqueda.")
    st.stop()

df = pd.DataFrame([{
    "ID": c["id"],
    "Empresa": c["name"],
    "Sector": c.get("sector", "N/D"),
    "Pais": c.get("country", "N/D"),
    "Creado": c.get("created_at", "N/D")[:10],
} for c in display_companies])

st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("📋 Ver Analisis Guardado")

company_options = {f"{c['name']} (ID:{c['id']})": c["id"] for c in display_companies}
selected = st.selectbox("Selecciona una empresa", list(company_options.keys()))

if selected:
    cid = company_options[selected]
    company_info = db.get_company(cid)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{company_info['name']}** | Sector: {company_info.get('sector', 'N/D')} | Pais: {company_info.get('country', 'N/D')}")
    with col2:
        if st.button("🗑️ Eliminar empresa", type="secondary"):
            db.delete_company(cid)
            st.success("Empresa eliminada.")
            st.rerun()

    analyses = db.get_analyses(cid)
    analysis_types = list({a["analysis_type"] for a in analyses})

    if not analyses:
        st.info("No hay analisis guardados para esta empresa.")
    else:
        tabs_map = {
            "financial": "📊 Financiero",
            "market": "🌍 Mercado",
            "competitive": "⚔️ Competitivo",
            "strategic": "🧠 Estrategico",
            "valuation": "💎 Valoracion",
            "enrichment": "🔍 Perfil",
            "report": "📝 Informe",
        }
        available = [t for t in tabs_map if t in analysis_types]
        if available:
            tab_labels = [tabs_map[t] for t in available]
            tabs = st.tabs(tab_labels)
            for tab, atype in zip(tabs, available):
                data = db.get_latest_analysis(cid, atype)
                with tab:
                    if data:
                        if atype == "report":
                            if data.get("executive_summary"):
                                st.markdown("**Resumen Ejecutivo**")
                                st.markdown(data["executive_summary"])
                            if data.get("report_text"):
                                with st.expander("Ver informe completo"):
                                    st.markdown(data["report_text"])
                        else:
                            st.json(data)
                    else:
                        st.info("Sin datos para este tipo de analisis.")

    st.markdown("---")
    if st.button("📄 Ir a Informes y Exportacion"):
        st.session_state["dashboard_selected_company_id"] = cid
        st.switch_page("pages/reports.py")
