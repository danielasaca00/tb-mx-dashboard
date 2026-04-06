#Inicio: Overview of available and analyzed data

#PAGE CONFIGURATION
import streamlit as st  #Website interface
import plotly.express as px #Interactive graphs
import plotly.graph_objects as go #Interactive graphs
import pandas as pd #Manage data tables
from db import get_resistance_profile, get_drug_resistance_counts, get_data_overview #Neo4j connection
from utils import render_sidebar #For sidebar

#Page Title
st.set_page_config(page_title="SVG-TB-MX", page_icon="🫁", layout="wide", initial_sidebar_state="expanded")

#Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, .kpi-value {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #E9EDE8;  
    border-right: 1px solid #d1dae3;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #000000  !important;
}

/* Main background */
.stApp {
    background: #E9EDE8;
}

/* KPI cards */
.kpi-card {
    background: #CBCDD1;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
}
.kpi-value {
    font-family: Inter, sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-label {
    font-size: 0.9rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7f93;
}
/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #0F0E0E;
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #000000;
}


/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

render_sidebar()

#Website Header
st.markdown("""
    <h1 style='font-family:Syne;font-size:2rem;color:#000000;margin-bottom:4px'>
        Tuberculosis en México : Vigilancia Genómica
    </h1>
    <p style='color:#4a6278;font-size:1.1rem;margin-bottom:0'>
        Sistema de vigilancina genómica de Mycobacterium tuberculosis en México a través de la integración de 
        información disponible en NCBI y la implementacion de TB Profiler para el análisis genómico. Modelado realizado
        en Neo4j y desarrollo de página web haciendo uso de Streamlit.
    </p>
""", unsafe_allow_html=True)

# DATA OVERVIEW
st.markdown("<div class='section-header'>Resumen General</div>", unsafe_allow_html=True)

with st.spinner("Cargando datos..."):
    overview = get_data_overview()

ov1, ov2, ov3, ov4, ov5, ov6, ov7 = st.columns(7)
overview_cards = [
    (ov1, overview["total_biosamples"],    "BioSamples totales",       "Muestras biológicas únicas registradas en NCBI"),
    (ov2, overview["total_sra_runs"],      "SRA disponibles",          "Total de SRA Run IDs registrados en NCBI para México"),
    (ov3, overview["runs_processed"],      "Runs procesados",          "Runs analizados con TB-Profiler v6"),
    (ov4, overview["qc_pass"],             "QC aprobado",              "Runs con cobertura y mapeo suficiente"),
    (ov5, overview["mdr"],                 "MDR-TB",                   "Muestras con resistencia a rifampicina e isoniacida"),
    (ov6, overview["xdr"],                 "XDR-TB",                   "Muestras con resistencia extensiva a fármacos"),
    (ov7, f"{overview['mdr_rate']}%",      "Tasa MDR",                 "Porcentaje MDR sobre muestras con QC aprobado"),
]
for col, val, label, tooltip in overview_cards:
    with col:
        st.markdown(f"""
        <div class='kpi-card' title="{tooltip}">
            <div class='kpi-value' style='color:#457345'>{val}</div>
            <div class='kpi-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#Pipeline funnel visualization
ov_left, ov_right = st.columns([1.4, 1])

with ov_left:
    funnel_fig = go.Figure(go.Funnel(
        y=["BioSamples totales", "SRA disponibles", "Runs procesados", "QC aprobado"],
        x=[
            overview["total_biosamples"],
            overview["total_sra_runs"],
            overview["runs_processed"],
            overview["qc_pass"],
        ],
        textinfo="value+percent initial",
        marker=dict(color=["#457345", "#5a8f5a", "#74a874", "#8ec48e"]),
        connector=dict(line=dict(color="#b0b8b0", width=1)),
        textfont=dict(color="#000000", size=12),
    ))
    funnel_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#000000", family="Inter"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=270,
    )
    st.plotly_chart(funnel_fig, use_container_width=True)

with ov_right:
    qc_pass     = overview["qc_pass"]
    qc_fail     = overview["qc_fail"]
    no_mtb      = overview.get("no_mtb", 0)
    failed_proc = overview.get("failed_processing", 0)
    empty_runs  = overview.get("empty_runs", 0)
    total_runs  = overview["total_sra_runs"]   # denominator for ALL percentages

    labels = ["QC aprobado", "QC rechazado", "No-Mtb", "No procesados", "Runs vacíos"]
    values = [qc_pass, qc_fail, no_mtb, failed_proc, empty_runs]
    colors = ["#457345", "#f97316", "#a855f7", "#ef4444", "#94a3b8"]

    # Percentages always over total_sra_runs, not over sum of displayed slices
    custom_text = [f"{round(v / total_runs * 100, 1)}%" for v in values]

    qc_fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        text=custom_text,
        textinfo="text",          # show our custom % instead of Plotly default
        hovertemplate="<b>%{label}</b><br>%{value} runs<br>%{text} de SRA disponibles<extra></extra>",
        marker=dict(
            colors=colors,
            line=dict(color="#3B3838", width=1.5),
        ),
        textposition="outside",
        textfont_size=10,
    ))
    qc_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#000000", family="Inter"),
        legend=dict(orientation="v", bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        margin=dict(t=10, b=10, l=10, r=10),
        height=270,
        annotations=[dict(
            text=f"<b>{total_runs}</b><br>SRA runs",
            x=0.5, y=0.5, font_size=11, font_color="#000000",
            showarrow=False,
        )],
    )
    st.plotly_chart(qc_fig, use_container_width=True)

    st.markdown(f"""
    <div style='font-size:0.78rem; color:#6b7f93; line-height:1.9; padding: 0 8px'>
        <b>{empty_runs}</b>&nbsp; ({round(empty_runs/total_runs*100,1)}%) Runs sin datos en SRA (spots = 0)<br>
        <b>{failed_proc}</b>&nbsp; ({round(failed_proc/total_runs*100,1)}%) Runs con error en TB-Profiler<br>
        <b>{no_mtb}</b>&nbsp; ({round(no_mtb/total_runs*100,1)}%) Runs sin <i>M. tuberculosis</i> confirmado<br>
        <b>{qc_fail}</b>&nbsp; ({round(qc_fail/total_runs*100,1)}%) Runs con baja cobertura o mapeo insuficiente<br>
        <b>{qc_pass}</b>&nbsp; ({round(qc_pass/total_runs*100,1)}%) Runs con QC aprobado ✓
    </div>
    """, unsafe_allow_html=True)

#Resistance Profile
st.markdown("<div class='section-header'>Perfil de Resistencia</div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.6])

with col_left:
    res_data = get_resistance_profile()
    df_res = pd.DataFrame(res_data)
    color_map = {
        "Sensitive"  : "#22c55e",
        "HR-TB"      : "#facc15",
        "MDR-TB"     : "#f97316",
        "RR-TB"      : "#fb923c",
        "Pre-XDR-TB" : "#ef4444",
        "XDR-TB"     : "#dc2626",
        "Other"      : "#64748b",
        "Low_coverage": "#334155",
    }
    fig = px.pie(
        df_res, values="count", names="drtype",
        color="drtype", color_discrete_map=color_map,
        hole=0.55,
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=11,
        marker=dict(line=dict(color="#3B3838", width=2)),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#000000", family="Inter"),
        legend=dict(
            orientation="v", bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        margin=dict(t=30, b=30, l=30, r=30),
        height=420,
        annotations=[dict(
            text=f"<b>{df_res['count'].sum()}</b><br>muestras",
            x=0.5, y=0.5, font_size=14, font_color="#000000",
            showarrow=False,
        )],
    )
    st.plotly_chart(fig, use_container_width=True)

#Drug counts
with col_right:
    drug_data = get_drug_resistance_counts()
    df_drug = pd.DataFrame(drug_data)
    class_colors = {
        "1st_line"           : "#f87171",
        "fluoroquinolone"    : "#fb923c",
        "group_A"            : "#e879f9",
        "group_B"            : "#a78bfa",
        "2nd_line_injectable": "#60a5fa",
        "1st_line_injectable": "#f59e0b",
        "other"              : "#64748b",
    }
    df_drug["color"] = df_drug["drug_class"].map(class_colors).fillna("#F20707")
    fig2 = go.Figure(go.Bar(
        x=df_drug["count"],
        y=df_drug["drug"],
        orientation="h",
        marker_color=df_drug["color"],
        text=df_drug["count"],
        textposition="outside",
        textfont=dict(color="#000000", size=11),
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#000000", family="Inter"),
        xaxis=dict(showgrid=True, gridcolor="#969090"),
        yaxis=dict(showgrid=False, autorange="reversed"),
        margin=dict(t=10, b=10, l=10, r=60),
        height=360,
    )
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.caption("2026 · Datos públicos NCBI ")
