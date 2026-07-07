"""Página Overview — Visión general de costes FinOPS.

4 KPI cards + 4 chart slots (stacked area, donut, treemap, gauge).
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_overview(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página Overview.

    Parameters
    ----------
    filters : dict[str, Any] | None
        Filtros activos del sidebar (currency, time_intelligence, etc.)
    """
    st.markdown(
        '<p class="page-title">Overview</p>'
        '<p class="page-subtitle">Visión general del gasto cloud</p>',
        unsafe_allow_html=True,
    )

    # ── KPI Cards ────────────────────────────────────────────────
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Total Coste</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Con datos reales en Fase 4</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with kpi2:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Distribución</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Compute · Storage · Transfer · AI</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with kpi3:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Balance</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Real vs Presupuesto</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with kpi4:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">TAG</div>'
            f'<div class="kpi-value">⏳ Próximamente</div>'
            f'<div class="kpi-trend">Tasa Anual de Gasto</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Chart Grid ───────────────────────────────────────────────
    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<div class="chart-card">'
            f'<div class="chart-title">Evolución del Gasto</div>'
            f'<div class="chart-placeholder">📈 Stacked Area Chart — Próximamente (Fase 3)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f'<div class="chart-card">'
            f'<div class="chart-title">Distribución por Servicio</div>'
            f'<div class="chart-placeholder">🍩 Donut Chart — Próximamente (Fase 3)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            f'<div class="chart-card">'
            f'<div class="chart-title">Detalle por Categoría</div>'
            f'<div class="chart-placeholder">🗂️ Treemap — Próximamente (Fase 3)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f'<div class="chart-card">'
            f'<div class="chart-title">Budget vs Actual</div>'
            f'<div class="chart-placeholder">🎯 Gauge Chart — Próximamente (Fase 3)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
