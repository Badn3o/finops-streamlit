"""Storage chart builders."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from charts.base import apply_finops_layout, empty_figure, fmt_value
from config.settings import LOGISTA_BLUE, LOGISTA_ORANGE, TRANSITION_COLORS


def build_storage_figures(
    kpis_df: pd.DataFrame,
    ranking_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    currency: str = "EUR",
) -> dict[str, go.Figure]:
    """Build the Storage dashboard figures."""
    return {
        "ranking": _build_ranking(ranking_df, currency),
        "trend": _build_trend(trend_df, currency),
        "donut": _build_donut(kpis_df, currency),
    }


def _build_ranking(ranking_df: pd.DataFrame, currency: str) -> go.Figure:
    if ranking_df.empty:
        return empty_figure("Sin datos para el ranking de bases de datos", height=380)

    df = ranking_df.copy().sort_values("cost_value", ascending=False).head(10)
    df = df.sort_values("cost_value")
    fig = go.Figure(
        go.Bar(
            x=df["cost_value"],
            y=df["DATABASE_NAME"],
            orientation="h",
            marker=dict(
                color=df["cost_value"],
                colorscale=[[0, LOGISTA_BLUE], [0.55, TRANSITION_COLORS["purple"]], [1, LOGISTA_ORANGE]],
                showscale=False,
            ),
            text=[fmt_value(v, currency) for v in df["cost_value"]],
            textposition="outside",
            hovertemplate="%{y}<br>%{x:,.2f} " + currency + "<extra></extra>",
        )
    )
    fig.update_layout(title=f"Ranking de bases de datos por coste ({currency})")
    fig.update_xaxes(tickformat=",.0f")
    return apply_finops_layout(fig, height=380, showlegend=False, hovermode="y")


def _build_trend(trend_df: pd.DataFrame, currency: str) -> go.Figure:
    if trend_df.empty:
        return empty_figure("Sin datos para la evolución storage", height=400)

    df = trend_df.copy().sort_values("period_start")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["database_tb"],
            name="Database TB",
            mode="lines",
            stackgroup="one",
            line=dict(color=LOGISTA_BLUE, width=1.5),
            hovertemplate="Database TB<br>%{x}<br>%{y:,.2f} TB<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["failsafe_tb"],
            name="Failsafe TB",
            mode="lines",
            stackgroup="one",
            line=dict(color=TRANSITION_COLORS["purple"], width=1.5),
            hovertemplate="Failsafe TB<br>%{x}<br>%{y:,.2f} TB<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["cost_value"],
            name=f"Coste {currency}",
            mode="lines+markers",
            line=dict(color=LOGISTA_ORANGE, width=3),
            marker=dict(color=LOGISTA_ORANGE, size=6),
            hovertemplate=f"Coste<br>%{{x}}<br>%{{y:,.2f}} {currency}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.update_layout(title=f"Evolución storage: coste y TB ({currency})")
    fig.update_yaxes(title_text="TB", secondary_y=False, tickformat=",.2f")
    fig.update_yaxes(title_text=f"Coste ({currency})", secondary_y=True, tickformat=",.0f")
    return apply_finops_layout(fig, height=400, showlegend=True, hovermode="x unified")


def _build_donut(kpis_df: pd.DataFrame, currency: str) -> go.Figure:
    if kpis_df.empty:
        return empty_figure("Sin datos para la composición de TB", height=360)

    row = kpis_df.iloc[0]
    database_tb = float(row.get("database_tb", 0.0) or 0.0)
    failsafe_tb = float(row.get("failsafe_tb", 0.0) or 0.0)
    active_tb = max(database_tb - failsafe_tb, 0.0)
    if active_tb <= 0 and failsafe_tb <= 0:
        return empty_figure("Sin TB disponibles", height=360)

    fig = go.Figure(
        go.Pie(
            labels=["Activo", "Failsafe"],
            values=[active_tb, failsafe_tb],
            hole=0.58,
            marker=dict(colors=[LOGISTA_BLUE, LOGISTA_ORANGE]),
            textinfo="percent+label",
        )
    )
    fig.update_traces(
        hovertemplate="%{label}<br>%{value:,.2f} TB<br>%{percent}<extra></extra>",
    )
    fig.update_layout(title=f"Distribución de TB activa vs failsafe ({currency})")
    return apply_finops_layout(fig, height=360, showlegend=True, hovermode="closest")
