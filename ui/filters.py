"""Filtros globales para el sidebar de FinOPS.

Centraliza los filtos de moneda, período, formato, business line y environment.
Se pueblan desde queries cacheadas a Snowflake cuando hay datos disponibles.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_sidebar_filters() -> dict[str, Any]:
    """Renderiza todos los filtros del sidebar y devuelve un dict con los valores activos.

    Returns
    -------
    dict[str, Any]
        Diccionario con: currency, time_intelligence, format,
        selected_business_lines, selected_environments
    """
    from config.settings import (
        CURRENCIES,
        DEFAULT_CURRENCY,
        DEFAULT_FORMAT,
        DEFAULT_TIME_INTELLIGENCE,
        FORMAT_OPTIONS,
        TIME_INTELLIGENCE_OPTIONS,
    )

    with st.sidebar:
        st.markdown(
            f'<div style="padding: 24px 0 8px; text-align: center;">'
            f'<span style="color: #8888AA; font-size: 11px; font-weight: 600; '
            f'text-transform: uppercase; letter-spacing: 1.5px;">Filtros</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Moneda
        currency = st.selectbox(
            "Moneda",
            options=CURRENCIES,
            index=CURRENCIES.index(
                st.session_state.get("currency", DEFAULT_CURRENCY)
            ),
            key="currency",
            label_visibility="collapsed",
        )

        # Time Intelligence / Período
        time_intelligence = st.selectbox(
            "Período",
            options=TIME_INTELLIGENCE_OPTIONS,
            index=TIME_INTELLIGENCE_OPTIONS.index(
                st.session_state.get("time_intelligence", DEFAULT_TIME_INTELLIGENCE)
            ),
            key="time_intelligence",
            label_visibility="collapsed",
        )

        # Formato
        fmt = st.selectbox(
            "Formato",
            options=FORMAT_OPTIONS,
            index=FORMAT_OPTIONS.index(
                st.session_state.get("format", DEFAULT_FORMAT)
            ),
            key="format",
            label_visibility="collapsed",
        )

        st.divider()

        # Business Line (multi-select, se puebla desde datos)
        st.markdown(
            '<div class="filter-label">Business Line</div>',
            unsafe_allow_html=True,
        )
        # Intentar cargar desde datos reales, fallback a ["All"]
        business_lines = _load_filter_options("business_line") or ["All"]
        selected_business_lines = st.multiselect(
            "Business Line",
            options=business_lines,
            default=st.session_state.get("selected_business_lines", ["All"]),
            key="selected_business_lines",
            label_visibility="collapsed",
        )

        # Environment
        st.markdown(
            '<div class="filter-label">Environment</div>',
            unsafe_allow_html=True,
        )
        environments = _load_filter_options("environment") or ["All"]
        selected_environments = st.multiselect(
            "Environment",
            options=environments,
            default=st.session_state.get("selected_environments", ["All"]),
            key="selected_environments",
            label_visibility="collapsed",
        )

    return {
        "currency": currency,
        "time_intelligence": time_intelligence,
        "format": fmt,
        "selected_business_lines": selected_business_lines,
        "selected_environments": selected_environments,
    }


@st.cache_data(ttl=3600)
def _load_filter_options(filter_type: str) -> list[str] | None:
    """Carga opciones de filtro desde Snowflake.

    Parameters
    ----------
    filter_type : str
        Tipo de filtro: "business_line" o "environment"

    Returns
    -------
    list[str] | None
        Lista de opciones únicas, o None si no hay datos
    """
    try:
        from db.connection import get_session
        from config.settings import DATABASE

        session = get_session()
        if filter_type == "business_line":
            result = session.sql(
                f"SELECT DISTINCT BUSINESS_LINE FROM {DATABASE}.FIN_OPS.DIM_BUSINESS_LINE ORDER BY BUSINESS_LINE"
            ).collect()
        else:
            result = session.sql(
                f"SELECT DISTINCT ENVIRONMENT FROM {DATABASE}.FIN_OPS.DIM_ENVIRONMENT ORDER BY ENVIRONMENT"
            ).collect()

        if result:
            return [r[0] for r in result]
        return None
    except Exception:
        return None
