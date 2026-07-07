"""Página Compute — Costes de cómputo Snowflake.

4 KPI cards + 3 chart slots.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_compute(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página Compute.

    Parameters
    ----------
    filters : dict[str, Any] | None
        Filtros activos del sidebar.
    """
    st.markdown(
        '<p class="page-title">Compute</p>'
        '<p class="page-subtitle">Costes de cómputo por warehouse</p>',
        unsafe_allow_html=True,
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Compute Coste</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )

    with kpi2:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Créditos</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )

    with kpi3:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Cloud Services %</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )

    with kpi4:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Warehouses</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Fase 4</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Coste por Warehouse</div>'
            f'<div class="chart-placeholder">📊 Horizontal Bar — Fase 3</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Cloud Services Ratio</div>'
            f'<div class="chart-placeholder">📈 Stacked Area — Fase 3</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="chart-card"><div class="chart-title">Créditos por Warehouse (Calendar Heatmap)</div>'
        f'<div class="chart-placeholder">🗓️ Heatmap — Fase 3</div></div>',
        unsafe_allow_html=True,
    )
