"""Streamlit App — FinOPS Control de Costes Cloud.

Router principal: inyecta CSS global, renderiza splash cover,
gestiona la navegación y carga la página activa.
"""

from __future__ import annotations

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
# SPLASH COVER (se muestra durante la carga inicial)
# ═══════════════════════════════════════════════════════════════════
if "initialized" not in st.session_state:
    st.session_state.initialized = False

if not st.session_state.initialized:
    cover = st.empty()
    with cover.container():
        from ui.cover import render_cover
        render_cover()

    # Marcar como inicializado después de un breve delay
    st.session_state.initialized = True
    cover.empty()
    st.rerun()

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
# ROUTER DE PÁGINAS
# ═══════════════════════════════════════════════════════════════════
page = st.session_state.get("page", "overview")


def render_page_filters() -> None:
    """Renderiza los filtros globales en el sidebar."""
    from config.settings import (
        CURRENCIES, TIME_INTELLIGENCE_OPTIONS, FORMAT_OPTIONS,
        DEFAULT_CURRENCY, DEFAULT_TIME_INTELLIGENCE, DEFAULT_FORMAT,
    )

    with st.sidebar:
        st.markdown(
            f'<div style="padding: 24px 0 8px; text-align: center;">'
            f'<span style="color: #8888AA; font-size: 11px; font-weight: 600; '
            f'text-transform: uppercase; letter-spacing: 1.5px;">Filtros</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Moneda ──
        st.selectbox(
            "Moneda",
            options=CURRENCIES,
            index=CURRENCIES.index(
                st.session_state.get("currency", DEFAULT_CURRENCY)
            ),
            key="currency",
            label_visibility="collapsed",
        )

        # ── Time Intelligence ──
        st.selectbox(
            "Período",
            options=TIME_INTELLIGENCE_OPTIONS,
            index=TIME_INTELLIGENCE_OPTIONS.index(
                st.session_state.get("time_intelligence", DEFAULT_TIME_INTELLIGENCE)
            ),
            key="time_intelligence",
            label_visibility="collapsed",
        )

        # ── Formato ──
        st.selectbox(
            "Formato",
            options=FORMAT_OPTIONS,
            index=FORMAT_OPTIONS.index(
                st.session_state.get("format", DEFAULT_FORMAT)
            ),
            key="format",
            label_visibility="collapsed",
        )

        st.divider()

        # ── Business Line (multi-select dinámico) ──
        st.markdown(
            '<div class="filter-label">Business Line</div>',
            unsafe_allow_html=True,
        )
        business_lines = st.session_state.get("business_lines", ["All"])
        selected_bl = st.multiselect(
            "Business Line",
            options=business_lines,
            default=st.session_state.get("selected_business_lines", ["All"]),
            key="selected_business_lines",
            label_visibility="collapsed",
        )

        # ── Environment ──
        st.markdown(
            '<div class="filter-label">Environment</div>',
            unsafe_allow_html=True,
        )
        environments = st.session_state.get("environments", ["All"])
        selected_env = st.multiselect(
            "Environment",
            options=environments,
            default=st.session_state.get("selected_environments", ["All"]),
            key="selected_environments",
            label_visibility="collapsed",
        )


# Renderizar sidebar de filtros
render_page_filters()

# ── Cargar la página activa ─────────────────────────────────────
if page == "overview":
    from pages.overview import render_overview
    render_overview()
elif page == "compute":
    from pages.compute import render_compute
    render_compute()
elif page == "storage":
    from pages.storage import render_storage
    render_storage()
elif page == "filetransfer":
    from pages.file_transfer import render_file_transfer
    render_file_transfer()
elif page == "ai":
    from pages.ai import render_ai
    render_ai()
else:
    from pages.overview import render_overview
    render_overview()
