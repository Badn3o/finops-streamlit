"""Página File Transfer — Costes de transferencia de datos.

3 KPI cards + 3 chart slots.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_file_transfer(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página File Transfer.

    Parameters
    ----------
    filters : dict[str, Any] | None
        Filtros activos del sidebar.
    """
    st.markdown(
        '<p class="page-title">File Transfer</p>'
        '<p class="page-subtitle">Costes de transferencia de datos</p>',
        unsafe_allow_html=True,
    )

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Volumen (TB)</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )
    with kpi2:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Coste EUR</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )
    with kpi3:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Coste USD</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Evolución Transferencia</div>'
            f'<div class="chart-placeholder">📈 Stacked Area — Fase 3</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Flujo por Tipo</div>'
            f'<div class="chart-placeholder">🔀 Sankey — Fase 3</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="chart-card"><div class="chart-title">Coste por Servicio de Transferencia</div>'
        f'<div class="chart-placeholder">📊 Horizontal Bar — Fase 3</div></div>',
        unsafe_allow_html=True,
    )
