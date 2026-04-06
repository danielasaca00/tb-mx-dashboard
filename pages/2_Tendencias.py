#Pages/2_Tendencias

#PAGE CONFIGURATION
import streamlit as st  #Website interface
import plotly.express as px #Interactive graphs
import plotly.graph_objects as go #Interactive graphs
import pandas as pd #Manage data tables
from db import get_mdr_trend, get_lineage_by_year #Neo4j connection to get data
from utils import render_sidebar #For sidebar

#Page title
st.set_page_config(page_title="Tendencias · TB México", page_icon="", layout="wide",initial_sidebar_state="expanded")

#Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');
.stApp { background: #E9EDE8; }
[data-testid="stSidebar"] { background: #E9EDE8; border-right: 1px solid #d1dae3; }
[data-testid="stSidebar"] * { color: #000000 !important; }
h1,h2,h3 { font-family: 'Inter', sans-serif !important; }
.section-header { font-family:'Inter',sans-serif;font-size:0.7rem;letter-spacing:.15em;
  text-transform:uppercase;color:#000000;margin:28px 0 16px;padding-bottom:8px;
  border-bottom:1px solid #1e2d3d; }
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:2rem}
</style>
""", unsafe_allow_html=True)

#Add sidebar
render_sidebar()

#Header
st.markdown("<h1 style='font-family:Syne;color:#000000;font-size:1.8rem'> Tendencias Temporales</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#4a6278'>Evolución de MDR y distribución de linajes por año</p>", unsafe_allow_html=True)

# INFO BLOCK 1: MDR Trend
st.markdown("<div class='section-header'>Tasa MDR por Año</div>", unsafe_allow_html=True)

with st.spinner("Cargando tendencias..."):
    trend_data = get_mdr_trend()

df_trend = pd.DataFrame(trend_data)

fig = go.Figure()

# Bar: total samples
fig.add_trace(go.Bar(
    x=df_trend["year"], y=df_trend["total"],
    name="Total muestras",
    marker_color="#1e2d3d",
    yaxis="y",
    hovertemplate="<b>%{x}</b><br>Total: %{y}<extra></extra>",
))

# Bar: MDR
fig.add_trace(go.Bar(
    x=df_trend["year"], y=df_trend["mdr"],
    name="MDR-TB",
    marker_color="#f87171",
    yaxis="y",
    hovertemplate="<b>%{x}</b><br>MDR: %{y}<extra></extra>",
))

# Line: MDR rate
fig.add_trace(go.Scatter(
    x=df_trend["year"], y=df_trend["mdr_rate"],
    name="Tasa MDR (%)",
    mode="lines+markers",
    line=dict(color="#00d4ff", width=2.5),
    marker=dict(size=7, color="#00d4ff"),
    yaxis="y2",
    hovertemplate="<b>%{x}</b><br>Tasa MDR: %{y}%<extra></extra>",
))

fig.update_layout(
    barmode="overlay",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c9d8e8", family="Inter"),
    xaxis=dict(
        showgrid=False, color="#4a6278",
        tickmode="linear", dtick=1,
    ),
    yaxis=dict(
        title="Número de muestras",
        showgrid=True, gridcolor="#1e2d3d",
        color="#4a6278",
    ),
    yaxis2=dict(
        title="Tasa MDR (%)",
        overlaying="y", side="right",
        showgrid=False, color="#00d4ff",
        range=[0, max(df_trend["mdr_rate"].max() * 1.3, 30)],
    ),
    legend=dict(
        orientation="h", y=1.08,
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    ),
    margin=dict(t=40, b=40, l=60, r=60),
    height=400,
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

#Annotation
max_year = df_trend.loc[df_trend["mdr_rate"].idxmax()]
st.info(f" Año con mayor tasa MDR: **{int(max_year['year'])}** — "
        f"{max_year['mdr_rate']}% ({int(max_year['mdr'])} de {int(max_year['total'])} muestras)")

#INFO BLOCK 2: Lineage by year
st.markdown("<div class='section-header'>Distribución de Linajes por Año</div>", unsafe_allow_html=True)

lin_data = get_lineage_by_year()
df_lin = pd.DataFrame(lin_data)

if not df_lin.empty:
    lineage_colors = {
        "lineage1": "#3b82f6",
        "lineage2": "#f59e0b",
        "lineage3": "#22c55e",
        "lineage4": "#00d4ff",
        "lineage5": "#a78bfa",
        "lineage6": "#f87171",
        "La1"     : "#fb923c",
        "La2"     : "#e879f9",
    }

    chart_type = st.radio(
        "Tipo de gráfica", ["Área apilada", "Barras apiladas"],
        horizontal=True, label_visibility="collapsed"
    )

    y_label = "Número de muestras"
    barnorm = None

    if chart_type == "Área apilada":
        fig2 = px.area(
            df_lin, x="year", y="n", color="lineage",
            color_discrete_map=lineage_colors,
            labels={"n": y_label, "year": "Año", "lineage": "Linaje"},
        )
        fig2.update_traces(line=dict(width=0.5))
    else:
        fig2 = px.bar(
            df_lin, x="year", y="n", color="lineage",
            color_discrete_map=lineage_colors,
            barmode="stack",
            labels={"n": y_label, "year": "Año", "lineage": "Linaje"},
        )


    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d8e8", family="Inter "),
        xaxis=dict(showgrid=False, color="#4a6278", tickmode="linear", dtick=1),
        yaxis=dict(showgrid=True, gridcolor="#1e2d3d", color="#4a6278", title=y_label),
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        margin=dict(t=40, b=40, l=60, r=20),
        height=380,
        hovermode="x unified",
    )
    st.plotly_chart(fig2, use_container_width=True)

# BLOCK 3: Raw table
with st.expander("Ver datos crudos de tendencias"):
    st.dataframe(
        df_trend.rename(columns={
            "year": "Año", "total": "Total",
            "mdr": "MDR", "mdr_rate": "Tasa MDR (%)"
        }),
        use_container_width=True, hide_index=True
    )

#Footer
st.markdown("---")
st.caption("2026 · Datos públicos NCBI ")