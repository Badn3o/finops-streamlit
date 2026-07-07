"""Compute chart builders."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from charts.base import COLORWAY, HEATMAP_SCALE, apply_finops_layout, empty_figure, fmt_value
from config.settings import LOGISTA_BLUE, LOGISTA_ORANGE, TRANSITION_COLORS


def build_compute_figures(
    kpis_df: pd.DataFrame,
    ranking_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    heatmap_df: pd.DataFrame,
    currency: str = "EUR",
) -> dict[str, go.Figure]:
    """Build the Compute dashboard figures."""
    return {
        "ranking": _build_ranking(ranking_df, currency),
        "trend": _build_trend(trend_df, currency),
        "heatmap": _build_heatmap(heatmap_df, currency),
    }


def _build_ranking(ranking_df: pd.DataFrame, currency: str) -> go.Figure:
    if ranking_df.empty:
        return empty_figure("Sin datos para el ranking de warehouses", height=380)

    df = ranking_df.copy().sort_values("cost_value", ascending=False).head(10)
    df = df.sort_values("cost_value")
    fig = go.Figure(
        go.Bar(
            x=df["cost_value"],
            y=df["WAREHOUSE_NAME"],
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
    fig.update_layout(title=f"Ranking de warehouses por coste ({currency})")
    fig.update_xaxes(tickformat=",.0f")
    return apply_finops_layout(fig, height=380, showlegend=False, hovermode="y")


def _build_trend(trend_df: pd.DataFrame, currency: str) -> go.Figure:
    if trend_df.empty:
        return empty_figure("Sin datos para la evolución compute", height=380)

    df = trend_df.copy().sort_values("period_start")
    fig = px.area(
        df,
        x="period_label",
        y="cost_value",
        color="COMPUTE_CATEGORY",
        color_discrete_sequence=COLORWAY,
        title=f"Evolución compute por categoría ({currency})",
    )
    fig.update_traces(
        hovertemplate="%{fullData.name}<br>%{x}<br>%{y:,.2f} " + currency + "<extra></extra>",
    )
    fig.update_layout(yaxis_title=f"Coste ({currency})")
    fig.update_yaxes(tickformat=",.0f")
    return apply_finops_layout(fig, height=380, showlegend=True, hovermode="x unified")


def _build_heatmap(heatmap_df: pd.DataFrame, currency: str) -> go.Figure:
    if heatmap_df.empty:
        return empty_figure("Sin datos para el heatmap diario", height=380)

    df = heatmap_df.copy()
    df["USAGE_DATE"] = pd.to_datetime(df["USAGE_DATE"], errors="coerce")
    df = df.dropna(subset=["USAGE_DATE"])
    if df.empty:
        return empty_figure("Sin fechas válidas para el heatmap", height=380)

    weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    df["month"] = df["USAGE_DATE"].dt.to_period("M").astype(str)
    df["weekday"] = df["USAGE_DATE"].dt.strftime("%a")
    pivot = (
        df.pivot_table(index="month", columns="weekday", values="cost_value", aggfunc="sum", fill_value=0)
        .reindex(columns=weekday_order)
    )
    if pivot.empty:
        return empty_figure("Sin datos agregados para el heatmap", height=380)

    fig = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=HEATMAP_SCALE,
            colorbar=dict(title=f"Coste {currency}"),
            hoverongaps=False,
        )
    )
    fig.update_traces(
        hovertemplate="Mes %{y}<br>Día %{x}<br>%{z:,.2f} " + currency + "<extra></extra>",
    )
    fig.update_layout(title=f"Heatmap diario de coste compute ({currency})")
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return apply_finops_layout(fig, height=380, showlegend=False, hovermode="closest")
