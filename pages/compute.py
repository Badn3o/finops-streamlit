"""Página Compute — Costes de cómputo Snowflake."""

from __future__ import annotations

from typing import Any

import streamlit as st

from charts.compute import build_compute_figures
from queries.compute import (
    get_compute_daily_heatmap,
    get_compute_kpis,
    get_compute_trend,
    get_warehouse_ranking,
)


def _currency_symbol(currency: str) -> str:
    return "€" if str(currency).upper() == "EUR" else "$"


def _fmt_money(value: float, currency: str) -> str:
    return f"{_currency_symbol(currency)}{value:,.2f}"


def _fmt_percent(value: float) -> str:
    return f"{value * 100:,.1f}%"


def _metric_card(label: str, value: str, trend: str | None = None, trend_class: str = "") -> None:
    delta_html = ""
    if trend:
        delta_html = f'<div class="kpi-delta {trend_class}">{trend}</div>'
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{delta_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_compute(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página Compute."""
    filters = filters or {}
    currency = str(filters.get("currency", "EUR")).upper()

    st.markdown(
        '<p class="page-title">Compute</p>'
        '<p class="page-subtitle">Costes de cómputo por warehouse y categoría real</p>',
        unsafe_allow_html=True,
    )

    kpis_df = get_compute_kpis(filters, currency=currency)
    ranking_df = get_warehouse_ranking(filters, currency=currency)
    trend_df = get_compute_trend(filters, currency=currency)
    heatmap_df = get_compute_daily_heatmap(filters, currency=currency)

    figures = build_compute_figures(
        kpis_df=kpis_df,
        ranking_df=ranking_df,
        trend_df=trend_df,
        heatmap_df=heatmap_df,
        currency=currency,
    )

    row = kpis_df.iloc[0] if not kpis_df.empty else {}
    compute_cost = float(row.get("compute_cost", 0.0) or 0.0)
    credits_used = float(row.get("credits_used", 0.0) or 0.0)
    cloud_ratio = float(row.get("cloud_ratio", 0.0) or 0.0)
    warehouse_count = float(row.get("warehouse_count", 0.0) or 0.0)
    compute_ratio = float(row.get("compute_ratio", 0.0) or 0.0)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        _metric_card("Compute Coste", _fmt_money(compute_cost, currency), f"{_fmt_percent(compute_ratio)} compute")
    with kpi2:
        _metric_card("Créditos usados", f"{credits_used:,.2f}", "Consumo real de cómputo")
    with kpi3:
        _metric_card("Cloud Services %", _fmt_percent(cloud_ratio), "Ratio cloud sobre total")
    with kpi4:
        _metric_card("Warehouses", f"{warehouse_count:,.0f}", "Activos en el rango")

    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures["ranking"], use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(figures["trend"], use_container_width=True, config={"displayModeBar": False})

    st.plotly_chart(figures["heatmap"], use_container_width=True, config={"displayModeBar": False})
