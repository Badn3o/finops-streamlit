"""Streamlit App — FinOPS Control de Costes Cloud.

Router principal: inyecta CSS global, gestiona splash cover,
sidebar de filtros, navegación y carga de páginas.
"""

from __future__ import annotations

import streamlit as st
from time import perf_counter, sleep

from ui.cover import render_cover
from ui.global_css import inject_global_css
from ui.header import render_header
from ui.filters import render_sidebar_filters

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
# SPLASH COVER (compatible con SiS: sin st.rerun() ni session_state)
# ═══════════════════════════════════════════════════════════════════
splash_placeholder = st.empty()
splash_started_at = perf_counter()
with splash_placeholder.container():
    render_cover()

try:
    # ═══════════════════════════════════════════════════════════════════
    # CSS GLOBAL (se inyecta una vez)
    # ═══════════════════════════════════════════════════════════════════
    inject_global_css()

    # ═══════════════════════════════════════════════════════════════════
    # HEADER DE NAVEGACIÓN
    # ═══════════════════════════════════════════════════════════════════
    render_header()

    # ═══════════════════════════════════════════════════════════════════
    # SIDEBAR DE FILTROS
    # ═══════════════════════════════════════════════════════════════════
    filters = render_sidebar_filters()

    # ═══════════════════════════════════════════════════════════════════
    # ROUTER DE PÁGINAS
    # ═══════════════════════════════════════════════════════════════════
    page = st.session_state.get("page", "overview")

    if page == "overview":
        from app_pages.overview import render_overview
        render_overview(filters=filters)
    elif page == "compute":
        from app_pages.compute import render_compute
        render_compute(filters=filters)
    elif page == "storage":
        from app_pages.storage import render_storage
        render_storage(filters=filters)
    elif page == "filetransfer":
        from app_pages.file_transfer import render_file_transfer
        render_file_transfer(filters=filters)
    elif page == "ai":
        from app_pages.ai import render_ai
        render_ai(filters=filters)
    else:
        from app_pages.overview import render_overview
        render_overview(filters=filters)
finally:
    # Deja que la portada se vea al menos un instante y evita el flash/cuadro
    # blanco inicial de SiS mientras hidrata la app.
    remaining = 1.2 - (perf_counter() - splash_started_at)
    if remaining > 0:
        sleep(remaining)
    splash_placeholder.empty()
