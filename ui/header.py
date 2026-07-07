"""Barra de navegación superior estilo NACEX.

Renderiza el header con logo Logista y tabs de navegación.
Usa st.navigation + st.Page para navegación nativa de Streamlit.
"""

from __future__ import annotations

import streamlit as st

from config.settings import PAGES
from ui.assets import LOGISTA_LOGO_NEG, get_page_icon


def render_header() -> None:
    """Renderiza el header de navegación superior con tabs nativos."""
    if "page" not in st.session_state:
        st.session_state.page = "overview"

    current = st.session_state.page

    # Construir HTML decorativo del header (solo visual, la navegación real usa st.navigation)
    nav_items_html = ""
    for page in PAGES:
        pid = page["id"]
        active = pid == current
        icon_svg = get_page_icon(pid, active=active)
        cls = "nav-item active" if active else "nav-item"

        nav_items_html += f"""
        <div class="{cls}" data-page="{pid}">
          {icon_svg}
          {page["label"]}
        </div>
        """

    logo_img = f'<img src="{LOGISTA_LOGO_NEG}" class="nav-logo" alt="Logista">'

    html = f"""
    <div class="nav-header">
      {logo_img}
      <div class="nav-items">
        {nav_items_html}
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    # Usar st.segmented_control como navegación funcional (oculto visualmente,
    # pero actualiza session_state correctamente)
    page_options = [p["id"] for p in PAGES]
    page_labels = [p["label"] for p in PAGES]

    selected = st.segmented_control(
        "Navegación",
        options=page_options,
        format_func=lambda x: page_labels[page_options.index(x)],
        default=current,
        key="nav_segment",
        label_visibility="collapsed",
        selection_mode="single",
    )

    if selected and selected != current:
        st.session_state.page = selected
        st.rerun()

    # Ocultar el segmented_control visualmente (se usa solo como backend de estado)
    st.markdown("""
    <style>
      div[data-testid="stSegmentedControl"] {
        display: none !important;
      }
    </style>
    """, unsafe_allow_html=True)
