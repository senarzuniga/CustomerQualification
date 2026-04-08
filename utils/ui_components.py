import streamlit as st

# ── Brand colours (mirrors .streamlit/config.toml) ──────────────────────────
PRIMARY = "#1F77B4"
SUCCESS = "#2ca02c"
WARNING = "#ff7f0e"
DANGER  = "#d62728"
NEUTRAL = "#7f7f7f"

CHART_PALETTE = [
    PRIMARY, "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
]


def metric_card(label: str, value: str, subtitle: str = "", color: str = PRIMARY) -> None:
    """Render a styled metric card with a coloured left border."""
    subtitle_html = (
        f"<div style='font-size:0.78rem;color:#888;margin-top:2px;'>{subtitle}</div>"
        if subtitle else ""
    )
    st.markdown(
        f"""
        <div style="
            background:white;
            border-left:4px solid {color};
            border-radius:6px;
            padding:12px 16px;
            box-shadow:0 1px 4px rgba(0,0,0,0.08);
            margin-bottom:8px;
        ">
            <div style="font-size:0.78rem;color:#666;text-transform:uppercase;
                        letter-spacing:0.05em;">{label}</div>
            <div style="font-size:1.6rem;font-weight:700;color:{color};
                        line-height:1.2;">{value}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def no_data_guide(next_page: str = "📤 Carga de Datos") -> None:
    """Render a consistent three-step empty-state guide."""
    st.warning("⚠️ **No hay datos disponibles.** Carga y procesa tu archivo primero.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"**Paso 1 →** Ve a **{next_page}** en el menú lateral")
    with c2:
        st.info("**Paso 2 →** Sube tu archivo Excel, CSV o PDF")
    with c3:
        st.info("**Paso 3 →** Haz clic en **🔄 Procesar Datos Ahora**")


def completeness_badge(pct: float) -> str:
    """Return a coloured emoji badge for a completeness percentage."""
    if pct >= 80:
        return f"🟢 {pct:.0f}%"
    elif pct >= 50:
        return f"🟡 {pct:.0f}%"
    return f"🔴 {pct:.0f}%"