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
from ui.kpi_card import render_kpi_card
from ui.tooltip import render_context_badges


def _currency_symbol(currency: str) -> str:
    return "€" if str(currency).upper() == "EUR" else "$"


def _fmt_money(value: float, currency: str) -> str:
    return f"{_currency_symbol(currency)}{value:,.2f}"


def _fmt_percent(value: float) -> str:
    return f"{value * 100:,.1f}%"


def render_compute(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página Compute."""
    filters = filters or {}
    currency = str(filters.get("currency", "EUR")).upper()

    st.markdown(
        '<p class="page-title fade-in stagger-1">Compute</p>'
        '<p class="page-subtitle fade-in stagger-2">Costes de cómputo por warehouse y categoría real</p>',
        unsafe_allow_html=True,
    )
    render_context_badges(
        [
            ("Warehouses", "Ranking real de warehouses por coste y créditos usados."),
            ("Cloud Services", "El ratio cloud services ayuda a detectar eficiencia y sobrecostes."),
            ("Heatmap diario", "Mapa de calor por día para localizar picos de consumo."),
        ]
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
        render_kpi_card(
            "Compute Coste",
            _fmt_money(compute_cost, currency),
            f"{_fmt_percent(compute_ratio)} compute",
            help_text="Coste total de Compute en el periodo filtrado.",
        )
    with kpi2:
        render_kpi_card(
            "Créditos usados",
            f"{credits_used:,.2f}",
            "Consumo real de cómputo",
            help_text="Créditos consumidos por los warehouses dentro del rango activo.",
        )
    with kpi3:
        render_kpi_card(
            "Cloud Services %",
            _fmt_percent(cloud_ratio),
            "Ratio cloud sobre total",
            help_text="Porcentaje de Cloud Services sobre el consumo total de Compute.",
        )
    with kpi4:
        render_kpi_card(
            "Warehouses",
            f"{warehouse_count:,.0f}",
            "Activos en el rango",
            help_text="Número de warehouses con actividad durante el periodo filtrado.",
        )

    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures["ranking"], use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(figures["trend"], use_container_width=True, config={"displayModeBar": False})

    st.plotly_chart(figures["heatmap"], use_container_width=True, config={"displayModeBar": False})
