#Pages/6_Database

import streamlit as st
from utils import render_sidebar, render_footer #For sidebar
from neo4j import GraphDatabase
import pandas as pd #dataframes


st.set_page_config(page_title="Base de datos", page_icon="x", layout="wide",initial_sidebar_state="expanded")

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

.stat-card {
    background: #ffffff;
    border: 1px solid #d1dae3;
    border-radius: 8px;
    padding: clamp(8px, 1.2vw, 20px) clamp(6px, 1vw, 24px);
    overflow: hidden;
    text-align: center;
}
.stat-number {
    font-family: 'Inter', sans-serif;
    font-size: clamp(1rem, 1.8vw, 2rem);
    word-break: break-word;
    font-weight: 700;
    color: #000000;
    line-height: 1;
}
.stat-label {
    font-family: 'Inter', sans-serif;
    font-size: clamp(0.55rem, 0.7vw, 0.72rem);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a6278;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

render_sidebar()

st.markdown("<h1 style='font-family:Syne;color:#000000;font-size:1.8rem'>Base de Datos</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#4a6278'>Grafo de vigilancia genómica de <em>Mycobacterium tuberculosis</em> en México, alojado en Neo4j AuraDB."
    "Neo4j es una base de datos de grafos de terceros que usa el lenguaje Cypher para consultar y visualizar datos. "
    "Permite hacer consultas avanzadas sin descargar nada, a través de su navegador público."
    "</p>",
    unsafe_allow_html=True)

# ── Neo4j connection ──────────────────────────────────────────────────
NEO4J_URI = st.secrets["NEO4J_URI"]
NEO4J_USER = st.secrets["NEO4J_USER"]
NEO4J_PASSWORD = st.secrets["NEO4J_PASSWORD"]


@st.cache_resource
def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


@st.cache_data(ttl=3600)  # Refreshes stats every hour automatically
def fetch_stats():
    driver = get_driver()
    with driver.session() as s:
        total_nodes = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        total_rels = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        rel_types = s.run("CALL db.relationshipTypes() YIELD relationshipType RETURN count(relationshipType) AS c").single()["c"]
        node_types = s.run("CALL db.labels() YIELD label RETURN count(label) AS c").single()["c"]
    return {
        "node_types": f"{node_types:,}",
        "total_nodes": f"{total_nodes:,}",
        "rel_types": f"{rel_types:,}",
        "total_rels": f"{total_rels:,}",
    }


# ── Stats ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Resumen</div>", unsafe_allow_html=True)

try:
    stats = fetch_stats()
    c1, c2, c3, c4= st.columns(4)
    for col, number, label in zip(
            [c1, c2, c3, c4],
            [stats["node_types"], stats["total_nodes"], stats["rel_types"], stats["total_rels"]],
            ["Tipos de nodos", "Nodos Totales","Tipos de Relaciones", "Relaciones Totales"],
    ):
        with col:
            st.markdown(
                f"<div class='stat-card'><div class='stat-number'>{number}</div>"
                f"<div class='stat-label'>{label}</div></div>",
                unsafe_allow_html=True,
            )
except Exception as e:
    st.warning(f"No se pudo conectar a Neo4j: {e}")

# ── Nodes table ───────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Nodos y propiedades</div>", unsafe_allow_html=True)

nodes_data = pd.DataFrame([
    ("SRARun", "run_id","run_id, spots (int), has_data (Yes/No), collection_date, isolation_source, state, lat , lon, "
    "lineage, sub_lineage,"" drtype, is_mdr, is_xdr, is_mtb, median_depth, pct_mapped, qc_pass, qc_warnings, fail_reasons, "
    "num_dr_variants, ""num_other_variants, tb_profiler_version, db_version"),
    ("BioSample", "biosample_id","biosample_id, publication_date, submission_date, status, sra_ids, owner, submitter, sample_name, strain"),
    ("Host", "host_id", "host_id, host_type, host_sex, host_age, host_disease"),
    ("Institution", "institution_id", "institution_id, name, submitter"),
    ("Location", "state", "state, country, lat, lon "),
    ("BioProject", "bioproject_id", "bioproject_id, study_id"),
    ("Lineage", "lineage_id", "lineage_id, top_level, description, sub_lineages, sample_count (int)"),
    ("TimePoint", "timepoint_id","timepoint_id, year, sample_count, mdr_count, mdr_rate"),
    ("Cluster", "cluster_id","cluster_id, size, mdr_count, mdr_rate, states, lineages, first_year, last_year ,span_years, sin singletons"),
    ("Drug", "name", "name, drug_class"),
    ("Mutation", "mutation_id","mutation_id, gene, aa_change, nt_change, variant_type, genome_pos, confidence, who_confidence, variant_class, drug"),
], columns=["Nodo", "Clave (Key)", "Propiedades"])

st.dataframe(nodes_data, use_container_width=True, hide_index=True,
             column_config={
                 "Nodo": st.column_config.TextColumn(width="small"),
                 "Clave (Key)": st.column_config.TextColumn(width="small"),
                 "Propiedades": st.column_config.TextColumn(width="large")
             }
             )

# ── Relationships table ───────────────────────────────────────────────
st.markdown("<div class='section-header'>Relaciones</div>", unsafe_allow_html=True)

rels_data = pd.DataFrame([
    ("BioSample", "[:HAS_RUN]", "SRARun", "—"),
    ("BioSample", "[:SUBMITTED_BY]", "Institution", "—"),
    ("SRARun", "[:FROM_HOST]", "Host", "—"),
    ("SRARun", "[:COLLECTED_IN]", "Location", "—"),
    ("SRARun", "[:PART_OF]", "BioProject", "—"),
    ("SRARun", "[:BELONGS_TO]", "Lineage", "—"),
    ("SRARun", "[:DETECTED_IN]", "TimePoint", "—"),
    ("SRARun", "[:IN_CLUSTER]", "Cluster", "—"),
    ("SRARun", "[:RESISTANT_TO]", "Drug", "confidence, who_confidence"),
    ("SRARun", "[:HAS_MUTATION]", "Mutation", "allele_freq (float), variant_depth (int), drug, variant_class"),
    ("Mutation", "[:CONFERS_RESISTANCE]", "Drug", "confidence, who_confidence"),
    ("SRARun", "[:LINKED_TO]", "SRARun", "snp_dist (int) ≤12 SNPs"),
    ("TimePoint", "[:NEXT]", "TimePoint", "— o"),
], columns=["Nodo de Origen", "Relación", "Nodo Final", "Propiedades"])

st.dataframe(rels_data, use_container_width=True, hide_index=True,
             column_config={
                 "Nodo de Origen": st.column_config.TextColumn(width="small"),
                 "Relación": st.column_config.TextColumn(width="small"),
                 "Nodo Final": st.column_config.TextColumn(width="small"),
                 "Propiedades": st.column_config.TextColumn(width="small"),
             }
             )

# ── Access ────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Acceso a la base de datos </div>", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stLinkButton"] a {
    background-color: #456E39 !important;
    border-color: #456E39 !important;
    color: #ffffff !important;
}
[data-testid="stLinkButton"] a:hover {
    background-color: #1a2a1a !important;
    border-color: #1a2a1a !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("")
col1, col2= st.columns([1, 1])
with col1:
    st.link_button("Abrir Neo4j Browser →", "https://browser.neo4j.io", type="primary")
with col2:
    st.link_button("Conoce más sobre Neo4j →", "https://neo4j.com/", type="secondary")


# ── Example queries ───────────────────────────────────────────────────
st.markdown("<div class='section-header'>Consultas de ejemplo</div>", unsafe_allow_html=True)

q1, q2 = st.columns(2)
with q1:
    st.markdown("**Tendencia MDR por año**")
    st.code("""MATCH (t:TimePoint)
WHERE t.sample_count > 0
RETURN t.year, t.mdr_rate
ORDER BY t.year""", language="cypher")

    st.markdown("**Linajes en un estado**")
    st.code("""MATCH (r:SRARun)-[:COLLECTED_IN]->(l:Location {state:'Guerrero'})
MATCH (r)-[:BELONGS_TO]->(lin:Lineage)
RETURN lin.lineage_id, count(r) AS n
ORDER BY n DESC""", language="cypher")

with q2:
    st.markdown("**Clústeres de transmisión activos**")
    st.code("""MATCH (c:Cluster)
WHERE c.mdr_rate > 0
RETURN c.cluster_id, c.size, c.states, c.mdr_rate
ORDER BY c.size DESC""", language="cypher")

    st.markdown("**Mutaciones más frecuentes**")
    st.code("""MATCH (r:SRARun)-[:HAS_MUTATION]->(m:Mutation)
RETURN m.gene, m.aa_change, count(r) AS n
ORDER BY n DESC LIMIT 10""", language="cypher")

# Footer
render_footer()