"""Barra de navegación superior estilo NACEX.

Renderiza el header con logo Logista y tabs de navegación.
Usa controles nativos de Streamlit para evitar que SiS escape HTML decorativo.
"""

from __future__ import annotations

import streamlit as st

from config.settings import PAGES
from ui.assets import LOGISTA_LOGO_NEG


def render_header() -> None:
    """Renderiza el header de navegación superior.

    En SiS, bloques grandes de HTML custom con SVG pueden aparecer como texto
    plano durante la hidratación o ante sanitización parcial. Por eso el header
    visual se limita a un contenedor estable y la navegación real/visible usa
    `st.segmented_control` nativo.
    """
    if "page" not in st.session_state:
        st.session_state.page = "overview"

    current = st.session_state.page
    logo_img = f'<img src="{LOGISTA_LOGO_NEG}" class="nav-logo" alt="Logista">'

    html = f"""
    <div class="nav-header">
      {logo_img}
      <div class="nav-title">Baikal | FinOps v1.0</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    # Navegación funcional y visible, sin HTML custom escapable.
    page_options = [p["id"] for p in PAGES]
    page_labels = {p["id"]: f'{p["icon"]} {p["label"]}' for p in PAGES}

    selected = st.segmented_control(
        "Navegación",
        options=page_options,
        format_func=lambda x: page_labels.get(x, x),
        default=current,
        key="nav_segment",
        label_visibility="collapsed",
        selection_mode="single",
    )

    if selected and selected != current:
        st.session_state.page = selected
        rerun = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
        if callable(rerun):
            rerun()

    st.markdown("""
    <style>
      div[data-testid="stSegmentedControl"] { padding: 10px 24px 8px; }
      div[data-testid="stSegmentedControl"] button {
        border-radius: 999px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.035) !important;
        color: #8888AA !important;
        font-weight: 700 !important;
      }
      div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
        background: rgba(252,76,2,0.16) !important;
        color: #FC4C02 !important;
        border-color: rgba(252,76,2,0.38) !important;
      }
    </style>
    """, unsafe_allow_html=True)
