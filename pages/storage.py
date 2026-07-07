"""Página Storage — Costes de almacenamiento Snowflake.

4 KPI cards + 3 chart slots.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_storage(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página Storage.

    Parameters
    ----------
    filters : dict[str, Any] | None
        Filtros activos del sidebar.
    """
    st.markdown(
        '<p class="page-title">Storage</p>'
        '<p class="page-subtitle">Costes de almacenamiento por base de datos</p>',
        unsafe_allow_html=True,
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Storage Coste</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )
    with kpi2:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">TB Totales</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )
    with kpi3:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Failsafe</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )
    with kpi4:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">% Total</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Coste por BD</div>'
            f'<div class="chart-placeholder">📊 Horizontal Bar — Fase 3</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Evolución Storage</div>'
            f'<div class="chart-placeholder">📈 Stacked Area — Fase 3</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="chart-card"><div class="chart-title">Distribución Failsafe vs Activo</div>'
        f'<div class="chart-placeholder">🍩 Donut — Fase 3</div></div>',
        unsafe_allow_html=True,
    )
