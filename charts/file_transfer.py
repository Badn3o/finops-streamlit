"""File transfer chart builders."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from charts.base import apply_finops_layout, empty_figure, fmt_value
from config.settings import LOGISTA_BLUE, LOGISTA_ORANGE, TRANSITION_COLORS


def build_transfer_figures(
    kpis_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    route_df: pd.DataFrame,
    flow_df: pd.DataFrame,
    currency: str = "EUR",
) -> dict[str, go.Figure]:
    """Build the File Transfer dashboard figures."""
    return {
        "trend": _build_trend(trend_df, currency),
        "flow": _build_flow(flow_df, currency),
        "ranking": _build_ranking(route_df, currency),
    }


def _build_trend(trend_df: pd.DataFrame, currency: str) -> go.Figure:
    if trend_df.empty:
        return empty_figure("Sin datos para la evolución de transferencias", height=380)

    df = trend_df.copy().sort_values("period_start")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["volume_gb"],
            name="Volumen GB",
            mode="lines",
            stackgroup="one",
            line=dict(color=LOGISTA_BLUE, width=1.4),
            hovertemplate="Volumen<br>%{x}<br>%{y:,.2f} GB<extra></extra>",
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
    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["billed_credits"],
            name="Créditos facturados",
            mode="lines",
            line=dict(color=TRANSITION_COLORS["purple"], width=2, dash="dot"),
            hovertemplate="Créditos facturados<br>%{x}<br>%{y:,.2f}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.update_layout(title=f"Evolución de transferencias ({currency})")
    fig.update_yaxes(title_text="Volumen (GB)", secondary_y=False)
    fig.update_yaxes(title_text=f"Coste ({currency}) / Créditos", secondary_y=True)
    fig.update_yaxes(tickformat=",.0f", secondary_y=False)
    fig.update_yaxes(tickformat=",.0f", secondary_y=True)
    return apply_finops_layout(fig, height=380, showlegend=True, hovermode="x unified")


def _build_flow(flow_df: pd.DataFrame, currency: str) -> go.Figure:
    if flow_df.empty:
        return empty_figure("Sin datos para el Sankey de transferencias", height=420)

    df = flow_df.copy()
    nodes: list[str] = []
    for value in pd.concat([df["source"], df["target"]], ignore_index=True).astype(str).tolist():
        if value not in nodes:
            nodes.append(value)
    index = {label: idx for idx, label in enumerate(nodes)}
    sources = [index[str(v)] for v in df["source"].astype(str)]
    targets = [index[str(v)] for v in df["target"].astype(str)]

    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=18,
                thickness=18,
                line=dict(color="rgba(255,255,255,0.2)", width=0.5),
                label=nodes,
                color=[LOGISTA_BLUE if i % 2 == 0 else LOGISTA_ORANGE for i in range(len(nodes))],
            ),
            link=dict(
                source=sources,
                target=targets,
                value=df["cost_value"],
                customdata=df["volume_gb"],
                color="rgba(252,76,2,0.35)",
                hovertemplate=(
                    "%{source.label} → %{target.label}<br>"
                    "Coste: %{value:,.2f} " + currency + "<br>"
                    "Volumen: %{customdata:,.2f} GB<extra></extra>"
                ),
            ),
        )
    )
    fig.update_layout(title=f"Flujo de transferencia por origen/destino ({currency})")
    return apply_finops_layout(fig, height=420, showlegend=False, hovermode="closest")


def _build_ranking(route_df: pd.DataFrame, currency: str) -> go.Figure:
    if route_df.empty:
        return empty_figure("Sin datos para el ranking de rutas", height=380)

    df = route_df.copy().sort_values("cost_value", ascending=False).head(10)
    df = df.sort_values("cost_value")
    route_label = (
        df["source_cloud"].astype(str)
        + ":"
        + df["source_region"].astype(str)
        + " → "
        + df["target_cloud"].astype(str)
        + ":"
        + df["target_region"].astype(str)
        + " · "
        + df["transfer_type"].astype(str)
    )
    fig = go.Figure(
        go.Bar(
            x=df["cost_value"],
            y=route_label,
            orientation="h",
            marker=dict(
                color=df["cost_value"],
                colorscale=[[0, LOGISTA_BLUE], [0.55, TRANSITION_COLORS["purple"]], [1, LOGISTA_ORANGE]],
                showscale=False,
            ),
            text=[fmt_value(v, currency) for v in df["cost_value"]],
            textposition="outside",
            hovertemplate="%{y}<br>%{x:,.2f} " + currency + "<br>%{customdata:,.2f} GB<extra></extra>",
            customdata=df["volume_gb"],
        )
    )
    fig.update_layout(title=f"Ranking de rutas por coste ({currency})")
    fig.update_xaxes(tickformat=",.0f")
    return apply_finops_layout(fig, height=380, showlegend=False, hovermode="y")
