"""Reusable KPI card component for FinOPS."""

from __future__ import annotations

from html import escape

import streamlit as st

_ALLOWED_TREND_CLASSES = {"", "positive", "negative"}


def render_kpi_card(
    label: str,
    value: str,
    trend: str | None = None,
    trend_class: str = "",
    help_text: str | None = None,
    value_suffix: str | None = None,
) -> None:
    """Render a branded KPI card with optional trend and hover help.

    The main value is always escaped. Use value_suffix for a small plain-text
    addendum (for example a currency or companion amount).
    """
    safe_trend_class = trend_class if trend_class in _ALLOWED_TREND_CLASSES else ""

    delta_html = ""
    if trend:
        delta_html = f'<div class="kpi-delta {safe_trend_class}">{escape(trend)}</div>'

    help_icon = ""
    title_attr = ""
    if help_text:
        escaped_help = escape(help_text)
        title_attr = f' title="{escaped_help}"'
        help_icon = (
            f'<span class="kpi-help" title="{escaped_help}" aria-label="{escaped_help}">'
            "ℹ"
            "</span>"
        )

    value_suffix_html = ""
    if value_suffix:
        value_suffix_html = f'<span class="kpi-unit">{escape(value_suffix)}</span>'

    st.markdown(
        f'<div class="kpi-card"{title_attr}>'
        f'<div class="kpi-label-row">'
        f'<div class="kpi-label">{escape(label)}</div>'
        f'{help_icon}'
        f'</div>'
        f'<div class="kpi-value">{escape(value)}{value_suffix_html}</div>'
        f'{delta_html}'
        f'</div>',
        unsafe_allow_html=True,
    )
