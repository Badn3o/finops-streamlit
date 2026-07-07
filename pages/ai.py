"""Página AI — Costes de servicios de IA/ML."""

from __future__ import annotations

from typing import Any

import streamlit as st

from charts.ai import build_ai_figures
from queries.ai import (
    get_ai_kpis,
    get_ai_service_breakdown,
    get_ai_trend,
    get_ai_user_ranking,
)
from ui.kpi_card import render_kpi_card
from ui.tooltip import render_context_badges


def _currency_symbol(currency: str) -> str:
    return "€" if str(currency).upper() == "EUR" else "$"


def _fmt_money(value: float, currency: str) -> str:
    return f"{_currency_symbol(currency)}{value:,.2f}"


def render_ai(filters: dict[str, Any] | None = None) -> None:
    """Renderiza la página AI."""
    filters = filters or {}
    currency = str(filters.get("currency", "EUR")).upper()

    st.markdown(
        '<p class="page-title">AI</p>'
        '<p class="page-subtitle">Consumo real de servicios de inteligencia artificial</p>',
        unsafe_allow_html=True,
    )
    render_context_badges(
        [
            ("Servicios IA", "Distribución por tipo de servicio consumido en Snowflake."),
            ("Tokens y créditos", "Créditos, tokens y token credits se comparan en el mismo rango temporal."),
            ("Ranking de usuarios", "Identifica qué usuarios concentran más coste de IA."),
        ]
    )

    kpis_eur = get_ai_kpis(filters, currency="EUR")
    kpis_usd = get_ai_kpis(filters, currency="USD")
    service_df = get_ai_service_breakdown(filters, currency=currency)
    trend_df = get_ai_trend(filters, currency=currency)
    user_ranking_df = get_ai_user_ranking(filters, currency=currency)

    figures = build_ai_figures(
        kpis_df=kpis_eur,
        service_df=service_df,
        trend_df=trend_df,
        user_ranking_df=user_ranking_df,
        currency=currency,
    )

    row_eur = kpis_eur.iloc[0] if not kpis_eur.empty else {}
    row_usd = kpis_usd.iloc[0] if not kpis_usd.empty else {}
    cost_eur = float(row_eur.get("cost_value", 0.0) or 0.0)
    cost_usd = float(row_usd.get("cost_value", 0.0) or 0.0)
    credits_used = float(row_eur.get("credits_used", 0.0) or 0.0)
    tokens = float(row_eur.get("tokens", 0.0) or 0.0)
    token_credits = float(row_eur.get("token_credits", 0.0) or 0.0)
    user_count = float(row_eur.get("user_count", 0.0) or 0.0)

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        render_kpi_card(
            "Coste EUR",
            _fmt_money(cost_eur, "EUR"),
            "Moneda base",
            help_text="Coste de IA expresado en EUR para el rango filtrado.",
        )
    with kpi2:
        render_kpi_card(
            "Coste USD",
            _fmt_money(cost_usd, "USD"),
            "Moneda secundaria",
            help_text="Coste de IA expresado en USD para contraste de conversión.",
        )
    with kpi3:
        render_kpi_card(
            "Créditos",
            f"{credits_used:,.2f}",
            "Crédito real usado",
            help_text="Créditos consumidos por servicios de IA/ML durante el periodo.",
        )
    with kpi4:
        render_kpi_card(
            "Tokens",
            f"{tokens:,.0f}",
            f"{token_credits:,.2f} token credits",
            help_text="Tokens procesados y sus créditos equivalentes dentro del rango activo.",
        )
    with kpi5:
        render_kpi_card(
            "Usuarios",
            f"{user_count:,.0f}",
            "Consumidores activos",
            help_text="Número de usuarios con consumo de IA en el periodo filtrado.",
        )

    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures["service_breakdown"], use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(figures["trend"], use_container_width=True, config={"displayModeBar": False})

    st.plotly_chart(figures["ranking"], use_container_width=True, config={"displayModeBar": False})
