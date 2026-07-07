"""Streamlit App — FinOPS Control de Costes Cloud.

Router principal: inyecta CSS global, gestiona splash cover,
sidebar de filtros, navegación y carga de páginas.
"""

from __future__ import annotations

import time

import streamlit as st

# ═══════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA (DEBE SER LA PRIMERA LLAMADA A STREAMLIT)
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FinOPS — Logista Costes Cloud",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
# SPLASH COVER (se muestra en el PRIMER render y desaparece en el
# SEGUNDO rerun, dando tiempo al navegador a pintarlo)
# ═══════════════════════════════════════════════════════════════════
if "splash_done" not in st.session_state:
    # Primer ciclo: mostrar cover
    placeholder = st.empty()
    with placeholder.container():
        from ui.cover import render_cover
        render_cover()

    st.session_state.splash_placeholder = placeholder
    st.session_state.splash_done = True
    time.sleep(0.5)
    st.rerun()

# Si el placeholder sigue vivo, vaciarlo (segundo ciclo)
if st.session_state.get("splash_placeholder"):
    st.session_state.splash_placeholder.empty()
    st.session_state.splash_placeholder = None

# ═══════════════════════════════════════════════════════════════════
# CSS GLOBAL (se inyecta una vez)
# ═══════════════════════════════════════════════════════════════════
from ui.global_css import inject_global_css
inject_global_css()

# ═══════════════════════════════════════════════════════════════════
# HEADER DE NAVEGACIÓN
# ═══════════════════════════════════════════════════════════════════
from ui.header import render_header
render_header()

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR DE FILTROS
# ═══════════════════════════════════════════════════════════════════
from ui.filters import render_sidebar_filters
filters = render_sidebar_filters()

# ═══════════════════════════════════════════════════════════════════
# ROUTER DE PÁGINAS
# ═══════════════════════════════════════════════════════════════════
page = st.session_state.get("page", "overview")

if page == "overview":
    from pages.overview import render_overview
    render_overview(filters=filters)
elif page == "compute":
    from pages.compute import render_compute
    render_compute(filters=filters)
elif page == "storage":
    from pages.storage import render_storage
    render_storage(filters=filters)
elif page == "filetransfer":
    from pages.file_transfer import render_file_transfer
    render_file_transfer(filters=filters)
elif page == "ai":
    from pages.ai import render_ai
    render_ai(filters=filters)
else:
    from pages.overview import render_overview
    render_overview(filters=filters)
