import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.session_manager import SessionManager
from utils.ui_components import no_data_guide

st.set_page_config(page_title="Analytics Avanzado", page_icon="📊", layout="wide")

SessionManager.init_session()

# ── Page header ────────────────────────────────────────────────────────────────
st.title("📊 Analytics Avanzado")
st.markdown("*Análisis detallado, filtros interactivos y correlaciones*")
st.markdown("---")

# ── Guard: no data ─────────────────────────────────────────────────────────────
if not SessionManager.has_data():
    no_data_guide()
    st.stop()

df_full = SessionManager.get_uploaded_data()


# ── Helpers ────────────────────────────────────────────────────────────────────
def _categorical_cols(frame: pd.DataFrame, max_unique_ratio: float = 0.7) -> list:
    result = []
    for col in frame.columns:
        if frame[col].dtype == object:
            n = frame[col].replace("", pd.NA).dropna().nunique()
            ratio = n / max(len(frame), 1)
            if 2 <= n and ratio <= max_unique_ratio:
                result.append((col, n))
    return [c for c, _ in sorted(result, key=lambda x: x[1])]


cat_cols = _categorical_cols(df_full)
num_cols = list(df_full.select_dtypes(include=np.number).columns)

# ── Sidebar Filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔎 Filtros Interactivos")
    st.caption("Selecciona valores para filtrar el dataset")

    filters: dict = {}
    for col in cat_cols[:5]:
        options = sorted(
            df_full[col].replace("", pd.NA).dropna().unique().tolist()
        )
        if options:
            selected = st.multiselect(
                col.replace("_", " ").title(),
                options=options,
                default=[],
                key=f"filter_{col}",
            )
            if selected:
                filters[col] = selected

    st.markdown("---")
    if st.button("🔄 Limpiar Filtros", use_container_width=True):
        for col in cat_cols[:5]:
            if f"filter_{col}" in st.session_state:
                st.session_state[f"filter_{col}"] = []
        st.rerun()

# Apply filters
df = df_full.copy()
for col, values in filters.items():
    df = df[df[col].isin(values)]

total = len(df_full)
filtered = len(df)

if filters:
    st.info(
        f"🔎 Mostrando **{filtered:,}** de **{total:,}** registros "
        f"({filtered / total * 100:.1f}%) con filtros activos"
    )
else:
    st.caption(f"📋 Mostrando todos los **{total:,}** registros")

# ── KPI Row ────────────────────────────────────────────────────────────────────
compl = (
    df.replace("", pd.NA).notna().mean().mean() * 100 if len(df) > 0 else 0.0
)
k1, k2, k3, k4 = st.columns(4)
k1.metric(
    "🗂 Registros Filtrados",
    f"{filtered:,}",
    delta=f"{filtered - total:,}" if filters else None,
)
k2.metric("📋 Columnas", len(df.columns))
k3.metric("✅ Completitud Promedio", f"{compl:.1f}%")
k4.metric("🔢 Columnas Numéricas", len(num_cols))

st.markdown("---")

# ── Column-level Analysis ──────────────────────────────────────────────────────
st.subheader("🔬 Análisis por Columna")

selected_col = st.selectbox(
    "Selecciona una columna para analizar:",
    options=list(df.columns),
    index=0,
    key="selected_col_analysis",
)

if selected_col:
    col_data = df[selected_col].replace("", pd.NA)
    chart_col, stats_col = st.columns([2, 1])

    with chart_col:
        if df[selected_col].dtype == object:
            counts = (
                col_data.dropna()
                .value_counts()
                .head(15)
                .reset_index()
            )
            counts.columns = [selected_col, "Cantidad"]
            fig = px.bar(
                counts,
                x=selected_col,
                y="Cantidad",
                title=f"Distribución: {selected_col.replace('_', ' ').title()}",
                color="Cantidad",
                color_continuous_scale="Blues",
                text="Cantidad",
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                height=370,
                showlegend=False,
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=45, b=80),
                xaxis_title="",
                yaxis_title="# Registros",
            )
            fig.update_xaxes(tickangle=-35)
            st.plotly_chart(fig, use_container_width=True)
        else:
            series = col_data.dropna()
            if len(series) > 0 and series.nunique() > 1:
                fig = px.histogram(
                    df,
                    x=selected_col,
                    nbins=25,
                    title=f"Distribución: {selected_col.replace('_', ' ').title()}",
                    color_discrete_sequence=["#1F77B4"],
                )
                fig.update_layout(
                    height=370,
                    bargap=0.05,
                    margin=dict(l=10, r=10, t=45, b=40),
                    xaxis_title=selected_col.replace("_", " ").title(),
                    yaxis_title="Frecuencia",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay suficiente variación en los datos para mostrar un gráfico.")

    with stats_col:
        st.markdown(f"**📋 Estadísticas: `{selected_col}`**")
        n_total = len(col_data)
        n_filled = int(col_data.notna().sum())
        n_empty = n_total - n_filled
        n_unique = int(col_data.dropna().nunique())

        st.metric("Total filas", f"{n_total:,}")
        st.metric("Con valor", f"{n_filled:,}")
        st.metric(
            "Vacíos",
            f"{n_empty:,}",
            delta=f"-{n_empty / n_total * 100:.1f}%" if n_empty > 0 else None,
            delta_color="inverse",
        )
        st.metric("Valores únicos", f"{n_unique:,}")

        if df[selected_col].dtype != object and n_filled > 0:
            st.metric("Promedio", f"{col_data.mean():.2f}")
            st.metric("Mediana", f"{col_data.median():.2f}")
            st.metric("Mín / Máx", f"{col_data.min():.2f} / {col_data.max():.2f}")

st.markdown("---")

# ── Completeness Table ─────────────────────────────────────────────────────────
st.subheader("📊 Completitud de Todas las Columnas")

comp_df = (
    df.replace("", pd.NA)
    .notna()
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
)
comp_df.columns = ["Campo", "Completitud (%)"]
comp_df["Estado"] = comp_df["Completitud (%)"].apply(
    lambda x: "✅ Alta" if x >= 80 else ("⚠️ Media" if x >= 50 else "❌ Baja")
)
comp_df = comp_df.sort_values("Completitud (%)", ascending=False)

st.dataframe(
    comp_df,
    use_container_width=True,
    column_config={
        "Campo": st.column_config.TextColumn("Campo"),
        "Completitud (%)": st.column_config.ProgressColumn(
            "Completitud",
            format="%.1f%%",
            min_value=0,
            max_value=100,
        ),
        "Estado": st.column_config.TextColumn("Estado"),
    },
    hide_index=True,
)

st.markdown("---")

# ── Numeric Correlation Heatmap ────────────────────────────────────────────────
if len(num_cols) >= 2:
    st.subheader("🔗 Correlación entre Variables Numéricas")
    st.caption(
        "Valores próximos a **1** (azul intenso) → correlación positiva. "
        "Próximos a **-1** (rojo intenso) → correlación negativa."
    )
    corr = df[num_cols].corr()
    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Matriz de Correlación",
        aspect="auto",
    )
    fig_corr.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")

# ── Searchable Data Table ──────────────────────────────────────────────────────
st.subheader("📋 Tabla de Datos")
st.caption(f"Mostrando hasta 500 de {filtered:,} registros del conjunto filtrado")

search = st.text_input(
    "🔍 Buscar en los datos:",
    placeholder="Escribe para filtrar filas…",
)
display_df = df.head(500)
if search:
    mask = (
        display_df.astype(str)
        .apply(lambda row: row.str.contains(search, case=False, na=False))
        .any(axis=1)
    )
    display_df = display_df[mask]
    st.caption(f"🔎 {len(display_df):,} fila(s) coinciden con «{search}»")

st.dataframe(display_df, use_container_width=True, height=450)

# Export filtered data
csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Descargar Datos Filtrados (CSV)",
    data=csv_bytes,
    file_name="datos_filtrados.csv",
    mime="text/csv",
    use_container_width=True,
)