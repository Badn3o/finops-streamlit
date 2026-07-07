"""Overview chart builders."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from charts.base import COLORWAY, apply_finops_layout, empty_figure, fmt_value
from config.settings import LOGISTA_BLUE, LOGISTA_ORANGE, SUCCESS, TOTAL_BALANCE_EUR, TRANSITION_COLORS


def build_overview_figures(
    kpis_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    distribution_df: pd.DataFrame,
    treemap_df: pd.DataFrame,
    balance_df: pd.DataFrame,
    currency: str = "EUR",
) -> dict[str, go.Figure]:
    """Build the Overview dashboard figures."""
    total_col = f"total_cost_{currency.lower()}"
    remaining_col = f"remaining_{currency.lower()}"
    total_cost = 0.0
    remaining_cost = 0.0
    if not kpis_df.empty:
        row = kpis_df.iloc[0]
        total_cost = float(row.get(total_col, row.get("total_cost_eur", 0.0)) or 0.0)
        remaining_cost = float(row.get(remaining_col, row.get("remaining_eur", 0.0)) or 0.0)
    if not balance_df.empty:
        row = balance_df.iloc[0]
        remaining_cost = float(row.get(remaining_col, remaining_cost) or remaining_cost)
    utilization = total_cost / (total_cost + remaining_cost) if (total_cost + remaining_cost) else 0.0

    return {
        "trend": _build_trend(trend_df, currency),
        "distribution": _build_distribution(distribution_df, currency),
        "treemap": _build_treemap(treemap_df, currency),
        "gauge": _build_gauge(utilization, total_cost, remaining_cost, currency),
    }


def _build_trend(trend_df: pd.DataFrame, currency: str) -> go.Figure:
    if trend_df.empty:
        return empty_figure("Sin datos para evolución del gasto", height=360)

    df = trend_df.copy().sort_values("period_start")
    fig = go.Figure()
    series = [
        ("compute_cost", "Compute", LOGISTA_BLUE),
        ("storage_cost", "Storage", TRANSITION_COLORS["purple"]),
        ("file_transfer_cost", "File Transfer", TRANSITION_COLORS["orange_dark"]),
        ("ai_cost", "AI", LOGISTA_ORANGE),
    ]
    for col, label, color in series:
        if col not in df.columns:
            continue
        fig.add_trace(
            go.Scatter(
                x=df["period_label"],
                y=df[col],
                name=label,
                mode="lines",
                stackgroup="one",
                line=dict(color=color, width=1.4),
                hovertemplate=f"{label}<br>%{{x}}<br>%{{y:,.2f}} {currency}<extra></extra>",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=df["period_label"],
            y=df["total_cost"],
            name="Total",
            mode="lines+markers",
            line=dict(color=SUCCESS, width=3),
            marker=dict(size=6, color=SUCCESS),
            hovertemplate=f"Total<br>%{{x}}<br>%{{y:,.2f}} {currency}<extra></extra>",
        )
    )
    fig.update_layout(title=f"Evolución del gasto cloud ({currency})")
    fig.update_yaxes(tickformat=",.0f")
    return apply_finops_layout(fig, height=360, showlegend=True, hovermode="x unified", y_title=f"Coste ({currency})")


def _build_distribution(distribution_df: pd.DataFrame, currency: str) -> go.Figure:
    if distribution_df.empty:
        return empty_figure("Sin datos para distribución por servicio", height=360)

    fig = px.pie(
        distribution_df,
        names="service_type",
        values="cost_value",
        hole=0.58,
        color_discrete_sequence=COLORWAY,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}<br>%{value:,.2f} " + currency + "<br>%{percent}<extra></extra>",
    )
    fig.update_layout(title=f"Distribución del gasto por servicio ({currency})")
    return apply_finops_layout(fig, height=360, showlegend=True, hovermode="closest")


def _build_treemap(treemap_df: pd.DataFrame, currency: str) -> go.Figure:
    if treemap_df.empty:
        return empty_figure("Sin datos para la jerarquía negocio → entorno → capa", height=380)

    fig = px.treemap(
        treemap_df,
        path=[px.Constant("FinOPS"), "business_line", "environment", "layer"],
        values="cost_value",
        color="cost_value",
        color_continuous_scale=[LOGISTA_BLUE, TRANSITION_COLORS["purple"], LOGISTA_ORANGE],
    )
    fig.update_traces(
        hovertemplate="%{label}<br>%{value:,.2f} " + currency + "<extra></extra>",
        textinfo="label+value",
    )
    fig.update_layout(title=f"Jerarquía negocio / entorno / capa ({currency})")
    return apply_finops_layout(fig, height=380, showlegend=False, hovermode="closest")


def _build_gauge(utilization: float, total_cost: float, remaining_cost: float, currency: str) -> go.Figure:
    budget = total_cost + remaining_cost
    base_total = budget if budget else TOTAL_BALANCE_EUR
    title = (
        f"Utilización del saldo ({currency})"
        f"<br><span style='font-size:12px;color:#8888AA'>"
        f"Gastado {fmt_value(total_cost, currency)} · Restante {fmt_value(remaining_cost, currency)} · Total {fmt_value(base_total, currency)}"
        f"</span>"
    )
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=utilization * 100.0,
            number={"suffix": "%", "valueformat": ".1f"},
            title={"text": title},
            gauge={
                "shape": "angular",
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "white"},
                "bar": {"color": LOGISTA_ORANGE, "thickness": 0.26},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 55], "color": "rgba(40,0,255,0.22)"},
                    {"range": [55, 80], "color": "rgba(106,19,203,0.22)"},
                    {"range": [80, 100], "color": "rgba(252,76,2,0.22)"},
                ],
                "threshold": {"line": {"color": SUCCESS, "width": 4}, "thickness": 0.7, "value": 85},
            },
        )
    )
    fig.update_layout(title=title)
    return apply_finops_layout(fig, height=360, showlegend=False, hovermode="closest")
