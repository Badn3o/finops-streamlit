"""AI chart builders."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from charts.base import COLORWAY, apply_finops_layout, empty_figure, fmt_value
from config.settings import LOGISTA_BLUE, LOGISTA_ORANGE, TRANSITION_COLORS


def build_ai_figures(
    kpis_df: pd.DataFrame,
    service_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    user_ranking_df: pd.DataFrame,
    currency: str = "EUR",
) -> dict[str, go.Figure]:
    """Build the AI dashboard figures."""
    return {
        "service_breakdown": _build_service_breakdown(service_df, currency),
        "trend": _build_trend(trend_df, currency),
        "ranking": _build_ranking(user_ranking_df, currency),
    }


def _build_service_breakdown(service_df: pd.DataFrame, currency: str) -> go.Figure:
    if service_df.empty:
        return empty_figure("Sin datos para el reparto por servicio AI", height=360)

    fig = go.Figure(
        go.Pie(
            labels=service_df["SERVICE_TYPE"],
            values=service_df["cost_value"],
            hole=0.58,
            marker=dict(colors=COLORWAY),
            textinfo="percent+label",
        )
    )
    fig.update_traces(
        hovertemplate="%{label}<br>%{value:,.2f} " + currency + "<br>%{percent}<extra></extra>",
    )
    fig.update_layout(title=f"Distribución del gasto AI por servicio ({currency})")
    return apply_finops_layout(fig, height=360, showlegend=True, hovermode="closest")


def _build_trend(trend_df: pd.DataFrame, currency: str) -> go.Figure:
    if trend_df.empty:
        return empty_figure("Sin datos para la evolución AI", height=380)

    df = trend_df.copy().sort_values("period_start")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["cost_value"],
            name=f"Coste {currency}",
            mode="lines",
            stackgroup="one",
            line=dict(color=LOGISTA_BLUE, width=1.8),
            hovertemplate=f"Coste<br>%{{x}}<br>%{{y:,.2f}} {currency}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["credits_used"],
            name="Créditos usados",
            mode="lines+markers",
            line=dict(color=LOGISTA_ORANGE, width=3),
            marker=dict(color=LOGISTA_ORANGE, size=6),
            hovertemplate="Créditos usados<br>%{x}<br>%{y:,.2f}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.update_layout(title=f"Evolución AI: coste y créditos ({currency})")
    fig.update_yaxes(title_text=f"Coste ({currency})", secondary_y=False, tickformat=",.0f")
    fig.update_yaxes(title_text="Créditos", secondary_y=True, tickformat=",.0f")
    return apply_finops_layout(fig, height=380, showlegend=True, hovermode="x unified")


def _build_ranking(user_ranking_df: pd.DataFrame, currency: str) -> go.Figure:
    if user_ranking_df.empty:
        return empty_figure("Sin datos para el ranking de usuarios", height=380)

    df = user_ranking_df.copy().sort_values("cost_value", ascending=False).head(10)
    df = df.sort_values("cost_value")
    fig = go.Figure(
        go.Bar(
            x=df["cost_value"],
            y=df["USER_NAME"],
            orientation="h",
            marker=dict(
                color=df["cost_value"],
                colorscale=[[0, LOGISTA_BLUE], [0.55, TRANSITION_COLORS["purple"]], [1, LOGISTA_ORANGE]],
                showscale=False,
            ),
            text=[fmt_value(v, currency) for v in df["cost_value"]],
            textposition="outside",
            customdata=df[["tokens", "usage_rows"]],
            hovertemplate="%{y}<br>%{x:,.2f} " + currency + "<br>Tokens %{customdata[0]:,.0f}<br>Usos %{customdata[1]:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(title=f"Ranking de usuarios por coste AI ({currency})")
    fig.update_xaxes(tickformat=",.0f")
    return apply_finops_layout(fig, height=380, showlegend=False, hovermode="y")
