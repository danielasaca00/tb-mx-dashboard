"""
pages/3_Linajes.py — Lineage distribution charts
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db import get_lineage_dist, get_cases_by_state, query
from utils import render_sidebar, render_footer #For sidebar

st.set_page_config(page_title="Linajes · TB México", page_icon="", layout="wide",initial_sidebar_state="expanded")

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

st.markdown("<h1 style='font-family:Syne;color:#000000;font-size:1.8rem'> Distribución de Linajes</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#4a6278'>Filogenia y distribución geográfica de linajes de M. tuberculosis en México</p>", unsafe_allow_html=True)

lineage_colors = {
    "lineage1": "#A327F5",
    "lineage2": "#f59e0b",
    "lineage3": "#22c55e",
    "lineage4": "#00d4ff",
    "lineage5": "#a78bfa",
    "lineage6": "#f87171",
    "La1"     : "#F54927",
    "La2"     : "#e879f9",
}

# ── Main distribution ─────────────────────────────────────────────────
st.markdown("<div class='section-header'>Distribución Global</div>", unsafe_allow_html=True)

lin_data = get_lineage_dist()
df_lin = pd.DataFrame(lin_data)
df_lin["lineage"] = df_lin["lineage"].apply(
    lambda x: x.split(";")[0] if isinstance(x, str) and ";" in x else x
)
df_lin = df_lin.groupby("lineage", as_index=False).agg({"count": "sum"})

# Ensure optional columns exist so downstream code does not KeyError
if "description" not in df_lin.columns:
    df_lin["description"] = df_lin["lineage"]
if "sub_lineages" not in df_lin.columns:
    df_lin["sub_lineages"] = "N/A"

col1, col2 = st.columns(2)

with col1:
    # Donut
    fig_donut = px.pie(
        df_lin, values="count", names="lineage",
        color="lineage", color_discrete_map=lineage_colors,
        hole=0.55,
        custom_data=["description"],
    )
    fig_donut.update_traces(
        textposition="outside",
        textfont_size=11,
        hovertemplate="<b>%{label}</b><br>%{customdata[0]}<br>Muestras: %{value}<br>%{percent}<extra></extra>",
        marker=dict(line=dict(color="#000000", width=2)),
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#000000", family="Inter"),
        legend=dict(orientation="v", bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        margin=dict(t=30, b=30, l=0, r=0),
        height=500,
        annotations=[dict(
            text=f"<b>{df_lin['count'].sum()}</b><br>genomas",
            x=0.5, y=0.5, font_size=13, font_color="#000000", showarrow=False,
        )],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    # Horizontal bar with sub-lineage info
    fig_bar = go.Figure(go.Bar(
        y=df_lin["lineage"],
        x=df_lin["count"],
        orientation="h",
        marker_color=[lineage_colors.get(l, "#64748b") for l in df_lin["lineage"]],
        text=df_lin["count"],
        textposition="outside",
        textfont=dict(color="#c9d8e8", size=11),
        customdata=df_lin[["description", "sub_lineages"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>%{customdata[0]}<br>"
            "Muestras: %{x}<br>"
            "Sub-linajes: %{customdata[1]}<extra></extra>"
        ),
    ))
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d8e8", family="Inter"),
        xaxis=dict(showgrid=True, gridcolor="#1e2d3d", color="#4a6278"),
        yaxis=dict(showgrid=False, color="#c9d8e8", autorange="reversed"),
        margin=dict(t=10, b=10, l=10, r=60),
        height=320,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Lineage detail table ──────────────────────────────────────────────
st.markdown("<div class='section-header'>Detalle de Linajes</div>", unsafe_allow_html=True)

df_display = df_lin[["lineage", "description", "count", "sub_lineages"]].copy()
df_display.columns = ["Linaje", "Descripción", "Muestras", "Sub-linajes observados"]

st.dataframe(
    df_display,
    use_container_width=True, hide_index=True,
    column_config={
        "Muestras": st.column_config.ProgressColumn(
            "Muestras", min_value=0, max_value=int(df_lin["count"].max())
        ),
    }
)
# Footer
render_footer()