"""Barra de navegación superior estilo NACEX.

Renderiza el header con logo Logista y tabs de navegación.
Usa session_state para controlar la página activa.
"""

from __future__ import annotations

import streamlit as st

from config.settings import PAGES, LOGISTA_ORANGE
from ui.assets import LOGISTA_LOGO_NEG, get_page_icon


def render_header() -> None:
    """Renderiza el header de navegación superior."""
    # Inicializar página activa
    if "page" not in st.session_state:
        st.session_state.page = "overview"

    current = st.session_state.page

    # Construir HTML del header
    nav_items_html = ""
    for page in PAGES:
        pid = page["id"]
        active = pid == current
        icon_svg = get_page_icon(pid, active=active)
        cls = "nav-item active" if active else "nav-item"

        nav_items_html += f"""
        <button class="{cls}" onclick="
          var pages = {{}};
          var el = this;
          var data = JSON.stringify({{page: '{pid}'}});
          fetch(window.location.href, {{
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            headers: {{'Content-Type': 'application/json'}},
            body: data
          }}).then(function() {{ el.closest('.nav-header').querySelectorAll('.nav-item').forEach(function(n) {{ n.classList.remove('active'); }}); el.classList.add('active'); }});
        ">
          {icon_svg}
          {page["label"]}
        </button>
        """

    # Logo Logista negativo (blanco sobre fondo oscuro)
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

    # Botones de Streamlit para cambiar página (ocultos, acción real)
    cols = st.columns(len(PAGES))
    for i, page in enumerate(PAGES):
        pid = page["id"]
        if pid == current:
            with cols[i]:
                st.button(
                    page["label"],
                    key=f"nav_{pid}",
                    use_container_width=True,
                    type="secondary",
                )
        else:
            with cols[i]:
                if st.button(
                    page["label"],
                    key=f"nav_{pid}",
                    use_container_width=True,
                ):
                    st.session_state.page = pid
                    st.rerun()

    # Ocultar los botones nativos de Streamlit via CSS
    hide_nav_buttons = """
    <style>
      div[data-testid="column"] button {
        display: none !important;
      }
    </style>
    """
    st.markdown(hide_nav_buttons, unsafe_allow_html=True)
