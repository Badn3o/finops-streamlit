"""Shared Plotly helpers for FinOPS charts."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

from config.settings import (
    ACCENT_PURPLE,
    BG_CARD,
    BG_CARD_HOVER,
    BG_DARK,
    LOGISTA_BLUE,
    LOGISTA_ORANGE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TRANSITION_COLORS,
)

COLORWAY = [
    LOGISTA_BLUE,
    TRANSITION_COLORS["blue_light"],
    ACCENT_PURPLE,
    TRANSITION_COLORS["purple_light"],
    TRANSITION_COLORS["magenta"],
    TRANSITION_COLORS["orange_dark"],
    LOGISTA_ORANGE,
    TRANSITION_COLORS["orange_light"],
]

HEATMAP_SCALE = [
    [0.0, "#101224"],
    [0.2, LOGISTA_BLUE],
    [0.45, TRANSITION_COLORS["purple"]],
    [0.7, TRANSITION_COLORS["orange_dark"]],
    [1.0, LOGISTA_ORANGE],
]


def empty_figure(message: str, height: int = 340) -> go.Figure:
    """Return a styled empty-state chart."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(color=TEXT_SECONDARY, size=14),
    )
    fig.update_layout(
        height=height,
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        margin=dict(l=24, r=24, t=56, b=24),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        title=dict(text=message, x=0.02, xanchor="left", font=dict(color=TEXT_PRIMARY, size=18)),
    )
    return fig


def apply_finops_layout(
    fig: go.Figure,
    title: str | None = None,
    height: int = 340,
    showlegend: bool = True,
    hovermode: str = "x unified",
    x_title: str | None = None,
    y_title: str | None = None,
) -> go.Figure:
    """Apply the Logista FinOPS visual style to a Plotly figure."""
    layout_kwargs: dict[str, Any] = dict(
        height=height,
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        margin=dict(l=24, r=24, t=64, b=24),
        font=dict(color=TEXT_PRIMARY, family="Segoe UI, Avenir, sans-serif", size=12),
        colorway=COLORWAY,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.0,
            font=dict(color=TEXT_SECONDARY, size=11),
        ),
        hovermode=hovermode,
        showlegend=showlegend,
        title=dict(
            text=title or "",
            x=0.02,
            xanchor="left",
            font=dict(color=TEXT_PRIMARY, size=18, family="Segoe UI, Avenir, sans-serif"),
        ),
        xaxis=dict(
            title=x_title,
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.14)",
            zerolinecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color=TEXT_SECONDARY),
        ),
        yaxis=dict(
            title=y_title,
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.14)",
            zerolinecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color=TEXT_SECONDARY),
        ),
    )
    fig.update_layout(**layout_kwargs)
    fig.update_xaxes(tickfont=dict(color=TEXT_SECONDARY))
    fig.update_yaxes(tickfont=dict(color=TEXT_SECONDARY))
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=BG_DARK,
            bordercolor=BG_CARD_HOVER,
            font=dict(color=TEXT_PRIMARY),
        )
    )
    return fig


def fmt_value(value: float, currency: str = "EUR", digits: int = 2) -> str:
    """Format a numeric value for KPI cards."""
    symbol = "€" if str(currency).upper() == "EUR" else "$"
    return f"{symbol}{value:,.{digits}f}"


def fmt_plain(value: float, digits: int = 2) -> str:
    """Format a plain numeric value for KPI cards."""
    return f"{value:,.{digits}f}"


def fmt_percent(value: float, digits: int = 1) -> str:
    """Format a ratio as percent."""
    return f"{value * 100:,.{digits}f}%"
