"""Página File Transfer — Costes de transferencia de datos."""

from __future__ import annotations

from typing import Any

import streamlit as st

from charts.file_transfer import build_transfer_figures
from queries.file_transfer import (
    get_transfer_flow,
    get_transfer_kpis,
    get_transfer_route_ranking,
    get_transfer_trend,
)


def _currency_symbol(currency: str) -> str:
    return "€" if str(currency).upper() == "EUR" else "$"


def _fmt_money(value: float, currency: str) -> str:
    return f"{_currency_symbol(currency)}{value:,.2f}"


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


def render_file_transfer(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página File Transfer."""
    filters = filters or {}
    currency = str(filters.get("currency", "EUR")).upper()

    st.markdown(
        '<p class="page-title">File Transfer</p>'
        '<p class="page-subtitle">Transferencias reales entre clouds y regiones</p>',
        unsafe_allow_html=True,
    )

    kpis_eur = get_transfer_kpis(filters, currency="EUR")
    kpis_usd = get_transfer_kpis(filters, currency="USD")
    trend_df = get_transfer_trend(filters, currency=currency)
    route_df = get_transfer_route_ranking(filters, currency=currency)
    flow_df = get_transfer_flow(filters, currency=currency)

    figures = build_transfer_figures(
        kpis_df=kpis_eur,
        trend_df=trend_df,
        route_df=route_df,
        flow_df=flow_df,
        currency=currency,
    )

    row_eur = kpis_eur.iloc[0] if not kpis_eur.empty else {}
    row_usd = kpis_usd.iloc[0] if not kpis_usd.empty else {}
    volume_gb = float(row_eur.get("volume_gb", 0.0) or 0.0)
    cost_eur = float(row_eur.get("transfer_cost", 0.0) or 0.0)
    cost_usd = float(row_usd.get("transfer_cost", 0.0) or 0.0)
    route_count = float(row_eur.get("route_count", 0.0) or 0.0)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        _metric_card("Volumen GB", f"{volume_gb:,.2f}", "Transferencia real")
    with kpi2:
        _metric_card("Coste EUR", _fmt_money(cost_eur, "EUR"), "Moneda base")
    with kpi3:
        _metric_card("Coste USD", _fmt_money(cost_usd, "USD"), "Moneda secundaria")
    with kpi4:
        _metric_card("Rutas", f"{route_count:,.0f}", "Combinaciones únicas")

    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures["trend"], use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(figures["flow"], use_container_width=True, config={"displayModeBar": False})

    st.plotly_chart(figures["ranking"], use_container_width=True, config={"displayModeBar": False})
