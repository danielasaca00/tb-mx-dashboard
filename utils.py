# utils.py — Componentes compartidos entre páginas

import streamlit as st
from datetime import datetime


def render_sidebar():
    """Renderiza sidebar con ancho ajustado"""

    # Fecha actual
    now = datetime.now()
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    fecha = f"{meses[now.month]} {now.year}"

    # CSS para ajustar solo el ancho del sidebar
    st.markdown(f"""
        <style>
        /* Ajustar ancho del sidebar */
        section[data-testid="stSidebar"] {{
            width: 16rem !important;
            min-width: 16rem !important;
            max-width: 16rem !important;
        }}

        section[data-testid="stSidebar"] > div {{
            width: 16rem !important;
            min-width: 16rem !important;
            max-width: 16rem !important;
        }}

        /* Info del sidebar */
        [data-testid="stSidebar"]::after {{
            content: "Datos: NCBI SRA\\A Análisis: TB-Profiler v6\\A Base: Neo4j\\A Actualizado: {fecha}";
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
        </style>
    """, unsafe_allow_html=True)


def render_footer():
    """Renderiza footer estándar para todas las páginas"""
    st.markdown("---")
    st.caption("Datos públicos NCBI · Página desarrollada en colaboración TB-IA UABC y UNICAL")


def render_page_components():
    """Renderiza sidebar y footer - usar en todas las páginas"""
    render_sidebar()