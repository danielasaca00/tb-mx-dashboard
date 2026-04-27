#Pages/7_Contacto

import streamlit as st
from utils import render_sidebar, render_footer #For sidebar


st.set_page_config(page_title="Sobre el Proyecto", page_icon="x", layout="wide", initial_sidebar_state="expanded")

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

st.markdown("""
    <h1 style='font-family:Syne;font-size:2rem;color:#000000;margin-bottom:4px'>
        Acerca del Proyecto
    </h1>
    <p style='color:#4a6278;font-size:1.1rem;margin-bottom:0'>
        Este dashboard forma parte de un esfuerzo colaborativo de vigilancia genómica de <i>Mycobacterium tuberculosis</i> 
        en México, desarrollado en el marco del Centro de Investigación, Innovación y Vigilancia Genómica de Enfermedades 
        Infecciosas (CIIViGEI) de la Universidad Autónoma de Baja California (UABC), Ensenada, Baja California, México.
    </p>
""", unsafe_allow_html=True)

#Equipo de Trabajo
st.markdown("<div class='section-header'>Equipo de Trabajo</div>", unsafe_allow_html=True)
st.markdown("""
    <p style='color:#4a6278;font-size:1.1rem;line-height:1.8'>

    <b>Dra. Raquel Muñiz-Salazar — Colaboradora Nacional</b><br>
    &nbsp;&nbsp;• Profesora-Investigadora, Escuela de Ciencias de la Salud, UABC<br>
    &nbsp;&nbsp;• Coordinadora de Investigación y Posgrado, ECS-UABC<br>
    &nbsp;&nbsp;• Coordinadora del CIIViGEI, UABC<br>
    &nbsp;&nbsp;• Presidenta de The Union Latinoamérica (2023–2026)<br>
    &nbsp;&nbsp;• Presidenta de RemiTB<br>

    <b>Dr. Giuseppe Pirrò — Colaborador Internacional</b><br>
    &nbsp;&nbsp;• Profesor Asociado, Ciencias de la Computación, Università della Calabria, Italia<br>
    &nbsp;&nbsp;• Departamento DEMACS (Ingegneria Informatica, Modellistica, Elettronica e Sistemistica)<br>
    &nbsp;&nbsp;• Áreas de investigación: Web Semántica, Bases de datos de grafos, Knowledge Graphs, Sistemas distribuidos<br>
        
    <b>Ing. Daniela Santana Camacho — Desarrollo y análisis de datos</b><br>
    &nbsp;&nbsp;• Bioingeniera, Universidad Autónoma de Baja California<br>
    &nbsp;&nbsp;• Estudiante de posgrado en Biotecnología de la Salud, DiBEST, Università della Calabria, Italia

    </p>
""", unsafe_allow_html=True)

#Recursos
st.markdown("<div class='section-header'>Recursos utilizados</div> ", unsafe_allow_html=True)
st.markdown("""
    <p style='color:#4a6278;font-size:1rem;line-height:2'>
    • <a href='https://www.ncbi.nlm.nih.gov/' target='_blank'>NCBI</a>: Recopilación de muestras y genomas<br>
    • <a href='https://github.com/jodyphelan/TBProfiler' target='_blank'>TB-Profiler</a>: Análisis genómico<br>
    • <a href='https://www.who.int/publications/i/item/9789240082410' target='_blank'>Catálogo de mutaciones de la OMS</a>: Clasificación de mutaciones y farmacorresistencia<br>
    • <a href='https://neo4j.com/' target='_blank'>Neo4j</a>: Base de datos<br>
    • <a href='https://streamlit.io/' target='_blank'>Streamlit</a>: Website framework
    </p>
""", unsafe_allow_html=True)

#Disclaimer
st.markdown("<div class='section-header'> Descargo de Responsabilidad</div> ", unsafe_allow_html=True)
st.markdown("""
    <p style='color:#4a6278;font-size:1rem;margin-bottom:0'>
    Esta herramienta es exclusivamente para fines de investigación científica. No ha sido aprobada, autorizada ni
    licenciada por ninguna autoridad reguladora. Los datos presentados no deben utilizarse como base para diagnóstico 
    clínico, tratamiento de pacientes ni ensayos clínicos en humanos. Al utilizar esta plataforma, el usuario reconoce
    y acepta estas condiciones.   <br><br>
    </p>
""", unsafe_allow_html=True)


# Footer
render_footer()
