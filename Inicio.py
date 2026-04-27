#Inicio: Overview of available and analyzed data

#PAGE CONFIGURATION
import streamlit as st  #Website interface
import plotly.graph_objects as go #Interactive graphs
from db import get_data_overview #Neo4j connection
from utils import render_sidebar, render_footer #For sidebar

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
    padding: clamp(8px, 1.2vw, 20px) clamp(6px, 1vw, 24px);
    text-align: center;
    overflow: hidden;
}
.kpi-value {
    font-family: Inter, sans-serif;
    font-size: clamp(1rem, 2vw, 2.8rem);
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
    word-break: break-word;
}
.kpi-label {
    font-size: clamp(0.55rem, 0.75vw, 0.9rem);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7f93;
    word-break: break-word;
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
        Sistema de vigilancia genómica de <i>Mycobacterium tuberculosis</i> en México a través de la integración de 
        información disponible en <a href="https://www.ncbi.nlm.nih.gov/" target="_blank" style="color:#2E86C1; 
        text-decoration:none;">NCBI</a> y la implementacion de <a href="https://tbdr.lshtm.ac.uk/" target="_blank" 
        style="color:#2E86C1; text-decoration:none;">TB Profiler</a> para el análisis genómico. Modelado realizado
        en Neo4j y desarrollo de página web haciendo uso de Streamlit.
    </p>
""", unsafe_allow_html=True)

# OBTENCION DE DATOS
st.markdown("<div class='section-header'>Obtención y análisis de datos</div>", unsafe_allow_html=True)
st.markdown("""
    <p style='color:#4a6278;font-size:1.1rem;margin-bottom:0'>
        1. Obtención de datos desde NCBI, aplicando filtros específicos para obtener muestras de Mtb proveniente de México  <br>
        2. Extracción de metadata relevante y accesos a SRA <br>
        3. Análisis genómico de SRA disponibles implemetando TB Profiler <br>
        4. Integración de metadata y resultados como nodos y relaciones para insertar en Neo4j <br>
        5. Análisis y visualización de datos a partir de queries <br>
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

# Footer
render_footer()
