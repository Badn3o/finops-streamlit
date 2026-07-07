"""Página Storage — Costes de almacenamiento Snowflake."""

from __future__ import annotations

from typing import Any

import streamlit as st

from charts.storage import build_storage_figures
from queries.storage import (
    get_database_ranking,
    get_storage_kpis,
    get_storage_trend,
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


def render_storage(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página Storage."""
    filters = filters or {}
    currency = str(filters.get("currency", "EUR")).upper()

    st.markdown(
        '<p class="page-title">Storage</p>'
        '<p class="page-subtitle">Costes de almacenamiento y capacidad real</p>',
        unsafe_allow_html=True,
    )

    kpis_df = get_storage_kpis(filters, currency=currency)
    ranking_df = get_database_ranking(filters, currency=currency)
    trend_df = get_storage_trend(filters, currency=currency)

    figures = build_storage_figures(
        kpis_df=kpis_df,
        ranking_df=ranking_df,
        trend_df=trend_df,
        currency=currency,
    )

    row = kpis_df.iloc[0] if not kpis_df.empty else {}
    storage_cost = float(row.get("storage_cost", 0.0) or 0.0)
    database_tb = float(row.get("database_tb", 0.0) or 0.0)
    failsafe_tb = float(row.get("failsafe_tb", 0.0) or 0.0)
    billable_tb = float(row.get("billable_tb", 0.0) or 0.0)
    active_tb = max(database_tb - failsafe_tb, 0.0)
    active_share = active_tb / database_tb if database_tb else 0.0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        _metric_card("Storage Coste", _fmt_money(storage_cost, currency), "Coste real acumulado")
    with kpi2:
        _metric_card("TB Totales", f"{database_tb:,.2f}", f"Activo {_fmt_percent(active_share)}")
    with kpi3:
        _metric_card("Failsafe", f"{failsafe_tb:,.2f}", "Capacidad protegida")
    with kpi4:
        _metric_card("Billable TB", f"{billable_tb:,.2f}", "TB facturables")

    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures["ranking"], use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(figures["trend"], use_container_width=True, config={"displayModeBar": False})

    st.plotly_chart(figures["donut"], use_container_width=True, config={"displayModeBar": False})
