import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.session_manager import SessionManager

SessionManager.init_session()

st.set_page_config(page_title="Analisis de Empresa", page_icon="🏢", layout="wide")


def run_analysis(company_name, sector, country, api_key):
    from agents.analysis_orchestrator import AnalysisOrchestrator
    orchestrator = AnalysisOrchestrator(api_key=api_key)
    return orchestrator.run_full_analysis(company_name, sector, country)


st.title("🏢 Analisis de Inteligencia Empresarial")
st.markdown("*Analisis completo de empresa con IA multi-agente*")
st.markdown("---")

with st.form("analysis_form"):
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("🏢 Nombre de la Empresa *", placeholder="Ej: Inditex, Mercadona, Telefonica...")
        sector = st.text_input("🏭 Sector (opcional)", placeholder="Ej: Retail, Tecnologia, Energia...")
    with col2:
        country = st.text_input("🌍 Pais (opcional)", placeholder="Ej: Espana, Mexico, Argentina...")
        api_key = st.text_input(
            "🔑 OpenAI API Key (opcional)", type="password",
            value=st.session_state.get("api_key", ""),
            help="Sin API Key se generaran datos estimados de ejemplo"
        )
    submitted = st.form_submit_button("🚀 Ejecutar Analisis Completo", type="primary", use_container_width=True)

if submitted and company_name:
    if api_key:
        st.session_state.api_key = api_key

    steps = [
        "🔍 Enriquecimiento de datos",
        "💰 Inteligencia financiera",
        "🌍 Inteligencia de mercado",
        "⚔️ Inteligencia competitiva",
        "🧠 Analisis estrategico",
        "💎 Valoracion y salida",
        "📝 Generacion de informe",
    ]

    progress_bar = st.progress(0)
    status_text = st.empty()

    with st.spinner("Ejecutando analisis multi-agente..."):
        for i, step_name in enumerate(steps):
            status_text.text(f"⏳ {step_name}...")
            progress_bar.progress(i / len(steps))
        results = run_analysis(company_name, sector, country, api_key)
        progress_bar.progress(1.0)
        status_text.text("✅ Analisis completado")

    st.session_state["last_analysis"] = results
    st.session_state["last_company"] = company_name

    st.success(f"✅ Analisis completo de **{company_name}** finalizado")

    if results.get("executive_summary"):
        with st.expander("📋 Resumen Ejecutivo", expanded=True):
            st.markdown(results["executive_summary"])

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Financiero", "🌍 Mercado", "⚔️ Competitivo", "🧠 Estrategico", "💎 Valoracion", "🚨 Analisis de Venta"
    ])

    with tab1:
        fin = results.get("financial", {})
        if fin:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 Ingresos", f"{fin.get('revenue', 'N/D')} M EUR")
            c2.metric("📈 EBITDA", f"{fin.get('ebitda', 'N/D')} M EUR")
            c3.metric("📊 Crecimiento", f"{fin.get('growth_rate', 'N/D')}%")
            c4.metric("💹 Margen", f"{fin.get('margin', 'N/D')}%")
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Datos financieros detallados**")
                for k, v in fin.items():
                    if k not in ["revenue_trend_3y", "error"] and v is not None:
                        st.write(f"- **{k}**: {v}")
            with c2:
                trend = fin.get("revenue_trend_3y", [])
                if trend and len(trend) == 3:
                    import pandas as pd
                    year = fin.get("year", 2024)
                    df_trend = pd.DataFrame({
                        "Anio": [str(year - 2), str(year - 1), str(year)],
                        "Ingresos (M EUR)": trend
                    })
                    st.markdown("**Evolucion de ingresos (3 anos)**")
                    st.bar_chart(df_trend.set_index("Anio"))
            if fin.get("reliability") == "BAJA" or fin.get("is_estimated"):
                st.info(f"ℹ️ Datos estimados. Fiabilidad: {fin.get('reliability', 'N/D')}")

    with tab2:
        mkt = results.get("market", {})
        if mkt:
            c1, c2, c3 = st.columns(3)
            c1.metric("📏 Tamano mercado", f"{mkt.get('market_size_bn', 'N/D')} Bn EUR")
            c2.metric("📈 Crecimiento", f"{mkt.get('market_growth_rate', 'N/D')}%")
            atr = mkt.get("market_attractiveness", "N/D")
            c3.metric("🏆 Atractivo", str(atr)[:20])
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Tendencias del mercado**")
                for t in mkt.get("trends", []):
                    st.write(f"- {t}")
                st.markdown("**Oportunidades**")
                for o in mkt.get("opportunities", []):
                    st.write(f"- {o}")
            with c2:
                st.markdown("**Barreras de entrada**")
                for b in mkt.get("entry_barriers", []):
                    st.write(f"- {b}")
                st.markdown("**Riesgos regulatorios**")
                for r in mkt.get("regulatory_risks", []):
                    st.write(f"- {r}")

    with tab3:
        comp = results.get("competitive", {})
        if comp:
            st.markdown(f"**Posicion en el mercado**: {comp.get('market_position', 'N/D')}")
            st.markdown(f"**Mapa competitivo**: {comp.get('competitive_map', 'N/D')}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Ventajas competitivas**")
                for a in comp.get("competitive_advantages", []):
                    st.success(f"✅ {a}")
            with c2:
                st.markdown("**Riesgos competitivos**")
                for r in comp.get("competitive_risks", []):
                    st.warning(f"⚠️ {r}")
            st.markdown("---")
            st.markdown("**Principales Competidores**")
            competitors = comp.get("competitors", [])
            if competitors:
                import pandas as pd
                comp_df = pd.DataFrame([{
                    "Competidor": c.get("name", "N/D"),
                    "Cuota": c.get("market_share", "N/D"),
                    "Fortalezas": ", ".join(c.get("strengths", [])),
                    "Debilidades": ", ".join(c.get("weaknesses", []))
                } for c in competitors])
                st.dataframe(comp_df, use_container_width=True)

    with tab4:
        strat = results.get("strategic", {})
        if strat:
            swot = strat.get("swot", {})
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**💪 Fortalezas**")
                for s in swot.get("strengths", []):
                    st.success(f"✅ {s}")
                st.markdown("**🚀 Oportunidades**")
                for o in swot.get("opportunities", []):
                    st.info(f"🔵 {o}")
            with c2:
                st.markdown("**⚠️ Debilidades**")
                for w in swot.get("weaknesses", []):
                    st.warning(f"⚠️ {w}")
                st.markdown("**🚨 Amenazas**")
                for t in swot.get("threats", []):
                    st.error(f"🔴 {t}")
            st.markdown("---")
            st.markdown("**Situacion actual**")
            st.write(strat.get("current_situation", "N/D"))
            st.markdown("**Trayectoria**")
            st.write(strat.get("trajectory", "N/D"))
            st.markdown("**Riesgos clave**")
            for r in strat.get("key_risks", []):
                st.write(f"- {r}")
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Escenarios 5 Anos**")
                s5 = strat.get("scenario_5y", {})
                st.success(f"Mejor caso: {s5.get('best', 'N/D')}")
                st.error(f"Peor caso: {s5.get('worst', 'N/D')}")
                st.info(f"Mas probable: {s5.get('most_likely', 'N/D')}")
            with c2:
                st.markdown("**Escenarios 10 Anos**")
                s10 = strat.get("scenario_10y", {})
                st.success(f"Mejor caso: {s10.get('best', 'N/D')}")
                st.error(f"Peor caso: {s10.get('worst', 'N/D')}")
                st.info(f"Mas probable: {s10.get('most_likely', 'N/D')}")

    with tab5:
        val = results.get("valuation", {}).get("valuation", {})
        if val:
            c1, c2, c3 = st.columns(3)
            c1.metric("💎 Valor Minimo", f"{val.get('min_value_m', 'N/D')} M EUR")
            c2.metric("💎 Valor Estimado", f"{val.get('estimated_value_m', 'N/D')} M EUR")
            c3.metric("💎 Valor Maximo", f"{val.get('max_value_m', 'N/D')} M EUR")
            st.markdown(f"**Metodologia**: {val.get('method', 'N/D')}")
            st.markdown(f"**Confianza**: {val.get('confidence', 'N/D')}")
            multiples = val.get("multiples_used", {})
            if multiples:
                st.markdown("**Multiples utilizados**")
                for k, v in multiples.items():
                    st.write(f"- {k}: {v}")

    with tab6:
        sale = results.get("valuation", {}).get("sale_propensity", {})
        if sale:
            prob = sale.get("probability", "Media")
            icon = "🟢" if prob == "Alta" else ("🟡" if prob == "Media" else "🔴")
            st.metric(f"{icon} Propension a la venta", prob)
            rec = sale.get("recommendation", "N/D")
            if rec == "Vender ahora":
                st.success(f"**Recomendacion**: {rec}")
            elif rec == "Preparar venta":
                st.warning(f"**Recomendacion**: {rec}")
            else:
                st.info(f"**Recomendacion**: {rec}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Razones principales**")
                for r in sale.get("main_reasons", []):
                    st.write(f"- {r}")
                st.markdown("**Compradores potenciales**")
                for b in sale.get("buyer_types", []):
                    st.write(f"- {b}")
            with c2:
                for grp_name, grp_key in [
                    ("Financieros", "financial_indicators"),
                    ("Estrategicos", "strategic_indicators"),
                    ("Organizacionales", "organizational_indicators"),
                    ("Contextuales", "contextual_indicators"),
                ]:
                    inds = sale.get(grp_key, {})
                    if inds:
                        st.markdown(f"**Indicadores {grp_name}**")
                        for k, v in inds.items():
                            st.write(f"- {k}: {v}")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Guardar en Base de Datos", type="primary"):
            try:
                from utils.database import CompanyDatabase
                db = CompanyDatabase()
                enrich = results.get("enrichment", {})
                cid = db.save_company(company_name, enrich.get("sector", sector), enrich.get("country", country))
                for atype in ["enrichment", "financial", "market", "competitive", "strategic", "valuation"]:
                    if atype in results:
                        db.save_analysis(cid, atype, results[atype])
                db.save_analysis(cid, "report", {
                    "executive_summary": results.get("executive_summary", ""),
                    "report_text": results.get("report_text", ""),
                })
                st.success(f"✅ Analisis guardado con ID: {cid}")
            except Exception as e:
                st.error(f"Error guardando: {e}")
    with c2:
        if st.button("📊 Ver Dashboard"):
            st.switch_page("pages/company_dashboard.py")

elif submitted and not company_name:
    st.error("❌ Por favor, introduce el nombre de la empresa")

if not submitted:
    st.info("👆 Introduce el nombre de una empresa y haz clic en 'Ejecutar Analisis Completo'")
    st.markdown("""
### 🤖 Agentes de Analisis Disponibles
| Agente | Descripcion |
|--------|-------------|
| 🔍 Enriquecimiento | Perfil completo, sector, tamano, productos |
| 💰 Financiero | Ingresos, EBITDA, crecimiento, tendencias |
| 🌍 Mercado | Tamano, tendencias, oportunidades |
| ⚔️ Competitivo | Competidores, ventajas, posicion |
| 🧠 Estrategico | SWOT, escenarios, riesgos |
| 💎 Valoracion | Valor estimado, multiples, metodologia |
| 🚨 Salida | Propension a venta, compradores, recomendacion |
""")
