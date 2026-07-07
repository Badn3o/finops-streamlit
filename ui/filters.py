"""Filtros globales para el sidebar de FinOPS.

Centraliza moneda, período, formato, business line, environment y rango de fechas.
Las opciones dinámicas se obtienen desde Snowflake con caché.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date, timedelta
from typing import Any

import streamlit as st


def _time_intelligence_range(selection: str) -> tuple[date, date]:
    """Map a time-intelligence label to a concrete date window."""
    today = date.today()
    sel = (selection or "6 MTD").upper()
    if sel in {"CURRENT", "MTD"}:
        return date(today.year, today.month, 1), today
    if sel == "6 MTD":
        return today - timedelta(days=183), today
    if sel == "YTD":
        return date(today.year, 1, 1), today
    if sel == "FYTD":
        fy_start_year = today.year if today.month >= 10 else today.year - 1
        return date(fy_start_year, 10, 1), today
    return today - timedelta(days=183), today


def _sync_date_range_from_time_intelligence() -> None:
    """Keep the date range aligned with the selected time intelligence."""
    selection = st.session_state.get("time_intelligence", "6 MTD")
    st.session_state["date_range"] = _time_intelligence_range(selection)
    st.session_state["_date_range_source"] = "auto"


def _mark_date_range_manual() -> None:
    """Mark the range as manually edited by the user."""
    st.session_state["_date_range_source"] = "manual"


def render_sidebar_filters() -> dict[str, Any]:
    """Renderiza todos los filtros del sidebar y devuelve un dict con los valores activos."""
    from config.settings import (
        CURRENCIES,
        DEFAULT_CURRENCY,
        DEFAULT_DATE_RANGE_MONTHS,
        DEFAULT_FORMAT,
        DEFAULT_TIME_INTELLIGENCE,
        FILTER_ALL,
        FORMAT_OPTIONS,
        TIME_INTELLIGENCE_OPTIONS,
    )

    today = date.today()
    default_start = today - timedelta(days=30 * DEFAULT_DATE_RANGE_MONTHS)
    auto_range = _time_intelligence_range(st.session_state.get("time_intelligence", DEFAULT_TIME_INTELLIGENCE))

    # Initialize / refresh date range if it is still auto-managed
    if "date_range" not in st.session_state or st.session_state.get("_date_range_source", "auto") != "manual":
        st.session_state["date_range"] = auto_range if st.session_state.get("time_intelligence") else (default_start, today)
        st.session_state["_date_range_source"] = "auto"

    with st.sidebar:
        st.markdown(
            f'<div style="padding: 24px 0 8px; text-align: center;">'
            f'<span style="color: #8888AA; font-size: 11px; font-weight: 600; '
            f'text-transform: uppercase; letter-spacing: 1.5px;">Filtros</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        currency = st.selectbox(
            "Moneda",
            options=CURRENCIES,
            index=CURRENCIES.index(st.session_state.get("currency", DEFAULT_CURRENCY)),
            key="currency",
            label_visibility="collapsed",
        )

        time_intelligence = st.selectbox(
            "Período",
            options=TIME_INTELLIGENCE_OPTIONS,
            index=TIME_INTELLIGENCE_OPTIONS.index(
                st.session_state.get("time_intelligence", DEFAULT_TIME_INTELLIGENCE)
            ),
            key="time_intelligence",
            label_visibility="collapsed",
            on_change=_sync_date_range_from_time_intelligence,
        )

        fmt = st.selectbox(
            "Formato",
            options=FORMAT_OPTIONS,
            index=FORMAT_OPTIONS.index(st.session_state.get("format", DEFAULT_FORMAT)),
            key="format",
            label_visibility="collapsed",
        )

        st.divider()

        # Business Line
        st.markdown('<div class="filter-label">Business Line</div>', unsafe_allow_html=True)
        business_lines = [FILTER_ALL] + _load_filter_options("business_line")
        selected_business_lines = st.multiselect(
            "Business Line",
            options=business_lines,
            default=st.session_state.get("selected_business_lines", [FILTER_ALL]),
            key="selected_business_lines",
            label_visibility="collapsed",
        )

        # Environment
        st.markdown('<div class="filter-label">Environment</div>', unsafe_allow_html=True)
        environments = [FILTER_ALL] + _load_filter_options("environment")
        selected_environments = st.multiselect(
            "Environment",
            options=environments,
            default=st.session_state.get("selected_environments", [FILTER_ALL]),
            key="selected_environments",
            label_visibility="collapsed",
        )

        st.markdown('<div class="filter-label">Rango fechas</div>', unsafe_allow_html=True)
        date_range = st.date_input(
            "Rango fechas",
            value=st.session_state.get("date_range", auto_range),
            key="date_range",
            label_visibility="collapsed",
            on_change=_mark_date_range_manual,
        )

    return {
        "currency": currency,
        "time_intelligence": time_intelligence,
        "format": fmt,
        "selected_business_lines": selected_business_lines,
        "selected_environments": selected_environments,
        "date_range": date_range,
    }


@st.cache_data(ttl=3600, show_spinner=False)
def _load_filter_options(filter_type: str) -> list[str]:
    """Carga opciones de filtro desde Snowflake, o lista vacía si no hay datos."""
    try:
        from config.settings import DATABASE, FINOPS_SCHEMA
        from db.connection import run_query_cached

        if filter_type == "business_line":
            sql = f"""
                SELECT DISTINCT BUSINESS_LINE AS VALUE
                FROM {DATABASE}.{FINOPS_SCHEMA}.FCT_BL_ENV_TAG_COST
                WHERE BUSINESS_LINE IS NOT NULL
                ORDER BY 1
            """
        else:
            sql = f"""
                SELECT DISTINCT ENVIRONMENT AS VALUE
                FROM {DATABASE}.{FINOPS_SCHEMA}.FCT_BL_ENV_TAG_COST
                WHERE ENVIRONMENT IS NOT NULL
                ORDER BY 1
            """

        result = run_query_cached(sql)
        return result.iloc[:, 0].astype(str).tolist() if not result.empty else []
    except Exception:
        return []
