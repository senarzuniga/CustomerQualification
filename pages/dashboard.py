import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.session_manager import SessionManager
from utils.ui_components import no_data_guide

st.set_page_config(page_title="Dashboard Ejecutivo", page_icon="📈", layout="wide")

SessionManager.init_session()

# ── Page header ────────────────────────────────────────────────────────────────
st.title("📈 Dashboard Ejecutivo")
st.markdown("*Vista consolidada de tu base de leads y clientes*")
st.markdown("---")

# ── Guard: no data ─────────────────────────────────────────────────────────────
if not SessionManager.has_data():
    no_data_guide()
    st.stop()

df = SessionManager.get_uploaded_data()


# ── Helper functions ───────────────────────────────────────────────────────────
def _overall_completeness(frame: pd.DataFrame) -> float:
    total = frame.shape[0] * frame.shape[1]
    if total == 0:
        return 0.0
    filled = frame.replace("", pd.NA).notna().sum().sum()
    return round(filled / total * 100, 1)


def _categorical_cols(frame: pd.DataFrame, max_cols: int = 6) -> list:
    """Return object columns with low-to-medium cardinality (good for charts)."""
    result = []
    for col in frame.columns:
        if frame[col].dtype == object:
            n_unique = frame[col].replace("", pd.NA).dropna().nunique()
            ratio = n_unique / max(len(frame), 1)
            if 2 <= n_unique and ratio <= 0.5:
                result.append(col)
    return result[:max_cols]


def _numeric_cols(frame: pd.DataFrame, max_cols: int = 4) -> list:
    return list(frame.select_dtypes(include=np.number).columns)[:max_cols]


# ── KPI Row ────────────────────────────────────────────────────────────────────
st.subheader("📊 Resumen General")

compl = _overall_completeness(df)
num_cols = _numeric_cols(df)
cat_cols = _categorical_cols(df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("🗂 Total Registros", f"{len(df):,}")
k2.metric("📋 Columnas", len(df.columns))
k3.metric(
    "✅ Completitud de Datos",
    f"{compl}%",
    delta="Alta" if compl >= 80 else ("Media" if compl >= 50 else "Baja"),
    delta_color="normal" if compl >= 80 else "inverse",
)
k4.metric("🔢 Columnas Numéricas", len(num_cols))

st.markdown("---")

# ── Data Quality Bar ───────────────────────────────────────────────────────────
st.subheader("🔍 Calidad de Datos por Columna")
st.caption("Porcentaje de valores presentes (no vacíos) en cada campo")

col_comp = (
    df.replace("", pd.NA)
    .notna()
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
)
col_comp.columns = ["Columna", "Completitud (%)"]
col_comp["Nivel"] = col_comp["Completitud (%)"].apply(
    lambda x: "Alta (≥80%)" if x >= 80 else ("Media (50-79%)" if x >= 50 else "Baja (<50%)")
)
col_comp = col_comp.sort_values("Completitud (%)", ascending=True)

color_map = {"Alta (≥80%)": "#2ca02c", "Media (50-79%)": "#ff7f0e", "Baja (<50%)": "#d62728"}

fig_quality = px.bar(
    col_comp,
    x="Completitud (%)",
    y="Columna",
    orientation="h",
    color="Nivel",
    color_discrete_map=color_map,
    text="Completitud (%)",
    title="Completitud por Columna",
    range_x=[0, 105],
)
fig_quality.update_traces(texttemplate="%{text}%", textposition="outside")
fig_quality.update_layout(
    height=max(300, len(df.columns) * 32),
    margin=dict(l=10, r=50, t=40, b=10),
    xaxis_title="Completitud (%)",
    yaxis_title="",
    legend_title="Nivel",
)
st.plotly_chart(fig_quality, use_container_width=True)

st.markdown("---")

# ── Categorical Distributions ──────────────────────────────────────────────────
if cat_cols:
    st.subheader("📊 Distribución de Categorías")
    st.caption("Frecuencia de los valores más comunes en los campos representativos")

    for i in range(0, len(cat_cols), 2):
        row = cat_cols[i : i + 2]
        cols = st.columns(len(row))
        for col, chart_col in zip(row, cols):
            with chart_col:
                counts = (
                    df[col]
                    .replace("", pd.NA)
                    .dropna()
                    .value_counts()
                    .head(10)
                    .reset_index()
                )
                counts.columns = [col, "Cantidad"]
                fig = px.bar(
                    counts,
                    x=col,
                    y="Cantidad",
                    title=f"Top valores: {col.replace('_', ' ').title()}",
                    color="Cantidad",
                    color_continuous_scale="Blues",
                    text="Cantidad",
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(
                    showlegend=False,
                    coloraxis_showscale=False,
                    height=340,
                    margin=dict(l=10, r=10, t=45, b=70),
                    xaxis_title="",
                    yaxis_title="# Registros",
                )
                fig.update_xaxes(tickangle=-30)
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

# ── Numeric Distributions ──────────────────────────────────────────────────────
if num_cols:
    st.subheader("📈 Distribución de Variables Numéricas")
    st.caption("Histogramas de los campos numéricos en tu dataset")

    for i in range(0, len(num_cols), 2):
        row = num_cols[i : i + 2]
        cols = st.columns(len(row))
        for col, chart_col in zip(row, cols):
            with chart_col:
                series = df[col].dropna()
                if series.nunique() < 2:
                    continue
                fig = px.histogram(
                    df,
                    x=col,
                    nbins=20,
                    title=f"Distribución: {col.replace('_', ' ').title()}",
                    color_discrete_sequence=["#1F77B4"],
                )
                fig.update_layout(
                    height=300,
                    margin=dict(l=10, r=10, t=45, b=40),
                    bargap=0.05,
                    xaxis_title=col.replace("_", " ").title(),
                    yaxis_title="Frecuencia",
                )
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

# ── Data Preview ───────────────────────────────────────────────────────────────
with st.expander("📋 Ver Datos Completos", expanded=False):
    st.caption(f"Mostrando hasta 100 de {len(df):,} registros")
    st.dataframe(df.head(100), use_container_width=True, height=400)

st.caption(
    f"Actualizado: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')} "
    f"| {len(df):,} registros totales"
)