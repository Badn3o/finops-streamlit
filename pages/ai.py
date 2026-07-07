"""Página AI — Costes de servicios de IA/ML.

5 KPI cards + 3 chart slots.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_ai(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página AI.

    Parameters
    ----------
    filters : dict[str, Any] | None
        Filtros activos del sidebar.
    """
    st.markdown(
        '<p class="page-title">AI</p>'
        '<p class="page-subtitle">Costes de servicios de inteligencia artificial</p>',
        unsafe_allow_html=True,
    )

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Coste EUR</div>'
            f'<div class="kpi-value">⏳ Próximamente</div></div>',
            unsafe_allow_html=True,
        )
    with kpi2:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Coste USD</div>'
            f'<div class="kpi-value">⏳ Próximamente</div></div>',
            unsafe_allow_html=True,
        )
    with kpi3:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Créditos</div>'
            f'<div class="kpi-value">⏳ Próximamente</div></div>',
            unsafe_allow_html=True,
        )
    with kpi4:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Tokens</div>'
            f'<div class="kpi-value">⏳ Próximamente</div></div>',
            unsafe_allow_html=True,
        )
    with kpi5:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Usuarios</div>'
            f'<div class="kpi-value">⏳ Próximamente</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Coste por Servicio AI</div>'
            f'<div class="chart-placeholder">📊 Horizontal Bar — Fase 3</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="chart-card"><div class="chart-title">Evolución Consumo</div>'
            f'<div class="chart-placeholder">📈 Stacked Area — Fase 3</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="chart-card"><div class="chart-title">Distribución por Modelo</div>'
        f'<div class="chart-placeholder">🍩 Donut — Fase 3</div></div>',
        unsafe_allow_html=True,
    )
