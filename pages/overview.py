"""Página Overview — Visión general de costes FinOPS."""

from __future__ import annotations

from typing import Any

import streamlit as st

from charts.overview import build_overview_figures
from queries.overview import (
    get_balance_summary,
    get_business_line_treemap,
    get_cost_distribution,
    get_monthly_trend,
    get_overview_kpis,
    get_tag_monthly_cost,
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


def render_overview(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página Overview."""
    filters = filters or {}
    currency = str(filters.get("currency", "EUR")).upper()

    st.markdown(
        '<p class="page-title">Overview</p>'
        '<p class="page-subtitle">Visión general del gasto cloud real desde Snowflake</p>',
        unsafe_allow_html=True,
    )

    kpis_df = get_overview_kpis(filters)
    trend_df = get_monthly_trend(filters, currency=currency)
    distribution_df = get_cost_distribution(filters, currency=currency)
    treemap_df = get_business_line_treemap(filters, currency=currency)
    balance_df = get_balance_summary(filters)
    tag_df = get_tag_monthly_cost(filters, currency=currency)

    figures = build_overview_figures(
        kpis_df=kpis_df,
        trend_df=trend_df,
        distribution_df=distribution_df,
        treemap_df=treemap_df,
        balance_df=balance_df,
        currency=currency,
    )

    row = kpis_df.iloc[0] if not kpis_df.empty else {}
    total_cost = float(row.get(f"total_cost_{currency.lower()}", row.get("total_cost_eur", 0.0)) or 0.0)
    remaining = float(row.get(f"remaining_{currency.lower()}", row.get("remaining_eur", 0.0)) or 0.0)
    compute_cost = float(row.get(f"compute_{currency.lower()}", row.get("compute_eur", 0.0)) or 0.0)
    top_service_share = compute_cost / total_cost if total_cost else 0.0
    utilization = total_cost / (total_cost + remaining) if (total_cost + remaining) else 0.0

    tag_name = "—"
    tag_value = 0.0
    if not tag_df.empty:
        tag_totals = tag_df.groupby("TAG_NAME", as_index=False)["cost_value"].sum().sort_values("cost_value", ascending=False)
        if not tag_totals.empty:
            top_tag = tag_totals.iloc[0]
            tag_name = str(top_tag["TAG_NAME"])
            tag_value = float(top_tag["cost_value"] or 0.0)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        _metric_card("Total Coste", _fmt_money(total_cost, currency), f"{_currency_symbol(currency)} {total_cost:,.2f} real")
    with kpi2:
        _metric_card("Compute Share", _fmt_percent(top_service_share), "Peso compute sobre el total")
    with kpi3:
        _metric_card("Saldo restante", _fmt_money(remaining, currency), f"Utilización {_fmt_percent(utilization)}")
    with kpi4:
        _metric_card("Top TAG", f"{tag_name}<span class='kpi-unit'>· {_fmt_money(tag_value, currency)}</span>")

    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures["trend"], use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(figures["distribution"], use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(figures["treemap"], use_container_width=True, config={"displayModeBar": False})
    with col4:
        st.plotly_chart(figures["gauge"], use_container_width=True, config={"displayModeBar": False})
