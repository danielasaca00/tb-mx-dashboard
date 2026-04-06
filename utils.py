# utils.py — Componentes compartidos entre páginas

import streamlit as st
from datetime import datetime

# Months in Spanish
_MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


def _fecha_actual() -> str:
    now = datetime.now()
    return f"{_MESES[now.month]} {now.year}"


def render_sidebar():
    if "sidebar_visible" not in st.session_state:
        st.session_state.sidebar_visible = True

    fecha = _fecha_actual()  # e.g. "Marzo 2026"

    st.markdown(f"""
        <style>
        [data-testid="stSidebar"]::after {{
            content: "Datos: NCBI SRA\\A Análisis genómico: TB-Profiler v6\\A Base de datos: Neo4j\\A Actualizado: {fecha}";
            white-space: pre;
            position: absolute;
            bottom: 1.5rem;
            left: 1rem;
            right: 1rem;
            font-size: 0.75rem;
            color: #524E4E;
            line-height: 2;
            border-top: 1px solid #d1dae3;
            padding-top: 0.6rem;
        }}

        div[data-testid="stButton"] button {{
            background: transparent !important;
            border: none !important;
            color: #457345 !important;
            font-size: 1.4rem !important;
            padding: 0 6px !important;
            line-height: 1 !important;
            box-shadow: none !important;
        }}
        div[data-testid="stButton"] button:hover {{
            color: #2f5230 !important;
            background: rgba(69,115,69,0.1) !important;
            border-radius: 6px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Show/hide
    if not st.session_state.sidebar_visible:
        st.markdown("""
        <style>
        [data-testid="stSidebar"]        { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        .main .block-container           { padding-left: 1rem !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        [data-testid="stSidebar"]        { display: flex !important; }
        [data-testid="collapsedControl"] { display: flex !important; }
        </style>
        """, unsafe_allow_html=True)


sidebar_toggle = render_sidebar
