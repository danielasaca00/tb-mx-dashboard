#Pages/1_Mapa. Distribución geográfica de las muestras

#PAGE CONFIGURATION
import streamlit as st  #Website interface
import plotly.graph_objects as go #Interactive graphs
import pandas as pd #Manage data tables
from db import get_cases_by_state #Neo4j connection, get data grouped by state
from utils import render_sidebar #For sidebar


#Page Title
st.set_page_config(page_title="Mapa · SVG-TB-MX", page_icon="", layout="wide",initial_sidebar_state="expanded")

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
st.markdown("<h1 style='font-family:Inter;color:#000000;font-size:1.8rem'> Distribución Geográfica</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#4a6278'>Muestras por estado</p>", unsafe_allow_html=True)

#BLOCK 1: MAP DISTRIBUTION
#Dropdown Menu
col_ctrl1,_ = st.columns([1, 4])
with col_ctrl1:
    metric = st.selectbox("Métrica", ["Total de muestras", "Casos MDR", "Casos XDR"])

colorscale = "YlOrRd"

#Data
with st.spinner("Cargando mapa..."):
    data = get_cases_by_state()

df = pd.DataFrame(data)

# Map display metric
metric_col = {"Total de muestras": "total", "Casos MDR": "mdr", "Casos XDR": "xdr"}[metric]

#Map
fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lat=df["lat"],
    lon=df["lon"],
    text=df["state"],
    hovertext=df.apply(lambda r: (
        f"<b>{r['state']}</b><br>"
        f"Total: {r['total']}<br>"
        f"MDR: {r['mdr']}<br>"
        f"XDR: {r['xdr']}"
    ), axis=1),
    hoverinfo="text",
    marker=dict(
        size=df[metric_col] ** 0.55 * 5,
        color=df[metric_col],
        colorscale=colorscale,
        showscale=True,
        colorbar=dict(
            title=dict(text=metric, font=dict(color="#000000")),
            thickness=12,
            len=0.5,
            bgcolor="rgba(0,0,0,0)",
            tickfont=dict(color="#000000"),
        ),
        line=dict(color="#0d1117", width=1),
        opacity=0.85,
        sizemode="area",
        sizemin=6,
    ),
    mode="markers+text",
    textposition="top center",
    textfont=dict(color="#000000", size=9),
))

fig.update_geos( #Map configuration
    visible=True,
    resolution=50,
    showcountries=True,
    countrycolor="#1e2d3d",
    showcoastlines=True,
    coastlinecolor="#1e2d3d",
    showland=True,
    landcolor="#9DD690",
    showocean=True,
    oceancolor="#84BFE3",
    showlakes=False,
    lataxis_range=[13, 33],
    lonaxis_range=[-120, -85],
    bgcolor="#0d1117",
)

fig.update_layout(
    paper_bgcolor="#E9EDE8",
    geo=dict(bgcolor="#0d1117"),
    font=dict(color="#c9d8e8", family="Inter"),
    margin=dict(t=10, b=10, l=0, r=0),
    height=520,
)

st.plotly_chart(fig, use_container_width=True)

#BLOCK 2: Data table per state
st.markdown("<div class='section-header'>Datos por Estado</div>", unsafe_allow_html=True)

df_display = df[["state", "total", "mdr", "xdr"]].copy()
df_display["mdr_rate"] = (df_display["mdr"] / df_display["total"] * 100).round(1).astype(str) + "%"
df_display.columns = ["Estado", "Total", "MDR", "XDR", "Tasa MDR"]
df_display = df_display.sort_values("Total", ascending=False).reset_index(drop=True)

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Total": st.column_config.NumberColumn("Total"),
        "MDR"  : st.column_config.NumberColumn("MDR", format="%d"),
        "XDR"  : st.column_config.NumberColumn("XDR", format="%d"),
    }
)

#Footer
st.markdown("---")
st.caption("2026 · Datos públicos NCBI ")