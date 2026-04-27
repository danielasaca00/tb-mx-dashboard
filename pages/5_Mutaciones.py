#Pages/2_Tendencias


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db import get_top_dr_mutations, get_mutation_network
from utils import render_sidebar, render_footer #For sidebar


st.set_page_config(page_title="Mutaciones · TB México", page_icon="", layout="wide", initial_sidebar_state="expanded")

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

st.markdown("<h1 style='font-family:Syne;color:#000000;font-size:1.8rem'> Mutaciones de Resistencia</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#4a6278'>Variantes genómicas que confieren resistencia a antibióticos anti-TB</p>", unsafe_allow_html=True)

drug_colors = {
    "isoniazid"   : "#f87171",
    "rifampicin"  : "#fb923c",
    "ethambutol"  : "#fbbf24",
    "pyrazinamide": "#a3e635",
    "streptomycin": "#34d399",
    "moxifloxacin": "#22d3ee",
    "levofloxacin": "#60a5fa",
    "bedaquiline" : "#a78bfa",
    "linezolid"   : "#e879f9",
    "amikacin"    : "#f472b6",
    "kanamycin"   : "#fb7185",
    "capreomycin" : "#c084fc",
    "ethionamide" : "#86efac",
    "clofazimine" : "#7dd3fc",
    "delamanid"   : "#fda4af",
}

# ── Controls ──────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    top_n = st.slider("Top N mutaciones", 10, 30, 20)
with col2:
    drug_filter = st.multiselect(
        "Filtrar por fármaco",
        options=list(drug_colors.keys()),
        default=[],
    )

# ── Top mutations bar chart ───────────────────────────────────────────
st.markdown("<div class='section-header'>Mutaciones Más Frecuentes</div>", unsafe_allow_html=True)

with st.spinner("Cargando mutaciones..."):
    mut_data = get_top_dr_mutations(limit=top_n)

df_mut = pd.DataFrame(mut_data)

if drug_filter:
    df_mut = df_mut[df_mut["drug"].isin(drug_filter)]

if not df_mut.empty:
    df_mut["label"] = df_mut["gene"] + " " + df_mut["aa_change"].fillna("")
    df_mut["color"] = df_mut["drug"].map(drug_colors).fillna("#64748b")

    fig = go.Figure(go.Bar(
        y=df_mut["label"],
        x=df_mut["sample_count"],
        orientation="h",
        marker_color=df_mut["color"],
        text=df_mut["sample_count"],
        textposition="outside",
        textfont=dict(color="#000000", size=10),
        customdata=df_mut[["drug", "who_confidence"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Fármaco: %{customdata[0]}<br>"
            "WHO confidence: %{customdata[1]}<br>"
            "Muestras: %{x}<extra></extra>"
        ),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d8e8", family="Inter"),
        xaxis=dict(showgrid=True, gridcolor="#1e2d3d", color="#4a6278", title="Número de muestras"),
        yaxis=dict(showgrid=False, color="#c9d8e8", autorange="reversed"),
        margin=dict(t=10, b=40, l=10, r=60),
        height=max(350, top_n * 22),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Mutation-Drug network ─────────────────────────────────────────────
st.markdown("<div class='section-header'>Red Mutación → Fármaco</div>", unsafe_allow_html=True)
st.caption("Cada nodo representa una mutación o fármaco. El tamaño indica el número de muestras.")

min_s = st.slider("Mínimo de muestras para mostrar mutación", 1, 20, 5)

net_data = get_mutation_network(min_samples=min_s)
df_net = pd.DataFrame(net_data)

if not df_net.empty:
    # Build network with plotly scatter
    import math

    genes = df_net["gene"].unique().tolist()
    drugs = df_net["drug"].unique().tolist()

    # Position genes in a circle, drugs in inner circle
    def circle_positions(items, radius, offset=0):
        n = len(items)
        positions = {}
        for i, item in enumerate(items):
            angle = 2 * math.pi * i / n + offset
            positions[item] = (radius * math.cos(angle), radius * math.sin(angle))
        return positions

    gene_pos = circle_positions(genes, radius=2)
    drug_pos = circle_positions(drugs, radius=0.8)

    # Edge traces
    edge_x, edge_y = [], []
    for _, row in df_net.iterrows():
        gx, gy = gene_pos[row["gene"]]
        dx, dy = drug_pos[row["drug"]]
        edge_x += [gx, dx, None]
        edge_y += [gy, dy, None]

    edges = go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=0.8, color="#1e3a5f"),
        hoverinfo="none",
        showlegend=False,
    )

    # Gene nodes
    gene_counts = df_net.groupby("gene")["sample_count"].sum()
    gene_nodes = go.Scatter(
        x=[gene_pos[g][0] for g in genes],
        y=[gene_pos[g][1] for g in genes],
        mode="markers+text",
        text=genes,
        textposition="top center",
        textfont=dict(color="#000000", size=10),
        marker=dict(
            size=[max(10, min(40, gene_counts.get(g, 1) ** 0.5 * 3)) for g in genes],
            color="#a78bfa",
            line=dict(color="#0d1117", width=1),
        ),
        hovertext=[f"{g}<br>{int(gene_counts.get(g,0))} muestras" for g in genes],
        hoverinfo="text",
        name="Gen",
    )

    # Drug nodes
    drug_counts = df_net.groupby("drug")["sample_count"].sum()
    drug_nodes = go.Scatter(
        x=[drug_pos[d][0] for d in drugs],
        y=[drug_pos[d][1] for d in drugs],
        mode="markers+text",
        text=drugs,
        textposition="bottom center",
        textfont=dict(color="#000000", size=10),
        marker=dict(
            size=[max(12, min(45, drug_counts.get(d, 1) ** 0.5 * 4)) for d in drugs],
            color=[drug_colors.get(d, "#64748b") for d in drugs],
            line=dict(color="#0d1117", width=1),
            symbol="diamond",
        ),
        hovertext=[f"{d}<br>{int(drug_counts.get(d,0))} muestras" for d in drugs],
        hoverinfo="text",
        name="Fármaco",
    )

    fig_net = go.Figure(data=[edges, gene_nodes, drug_nodes])
    fig_net.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#000000", family="Inter"),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        legend=dict(
            orientation="h", y=1.05, bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        margin=dict(t=20, b=20, l=20, r=20),
        height=520,
    )
    st.plotly_chart(fig_net, use_container_width=True)

# ── Heatmap: gene × drug ──────────────────────────────────────────────
st.markdown("<div class='section-header'>Heatmap Gen × Fármaco</div>", unsafe_allow_html=True)

if not df_net.empty:
    pivot = df_net.pivot_table(
        index="gene", columns="drug", values="sample_count",
        aggfunc="sum", fill_value=0
    )
    fig_heat = px.imshow(
        pivot,
        color_continuous_scale="Blues",
        labels=dict(x="Fármaco", y="Gen", color="Muestras"),
        aspect="auto",
    )
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d8e8", family="Inter"),
        xaxis=dict(color="#c9d8e8", tickangle=-35),
        yaxis=dict(color="#c9d8e8"),
        coloraxis_colorbar=dict(tickfont=dict(color="#c9d8e8"), title="Muestras"),
        margin=dict(t=10, b=80, l=80, r=20),
        height=380,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ── Table ─────────────────────────────────────────────────────────────
with st.expander("Ver tabla completa de mutaciones DR"):
    st.dataframe(
        df_mut[["label", "drug", "who_confidence", "sample_count"]].rename(columns={
            "label": "Mutación", "drug": "Fármaco",
            "who_confidence": "WHO Confidence", "sample_count": "Muestras"
        }),
        use_container_width=True, hide_index=True,
    )
# Footer
render_footer()