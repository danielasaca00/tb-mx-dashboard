#Pages/7_Contacto

import streamlit as st
from utils import render_sidebar #For sidebar


st.set_page_config(page_title="Contacto", page_icon="x", layout="wide", initial_sidebar_state="expanded")

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

st.markdown("<h1 style='font-family:Syne;color:#000000;font-size:1.8rem'>Contacto</h1>", unsafe_allow_html=True)

# ── MDR Trend ─────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Dudas y/o Comentarios</div>", unsafe_allow_html=True)


st.markdown("<div class='section-header'>Someter muestras</div>", unsafe_allow_html=True)


st.caption("2026 · Datos públicos NCBI · Página desarrollada en colaboración TB-IA UABC y UNICAL ")
