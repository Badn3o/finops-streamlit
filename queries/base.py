"""Shared SQL helpers for FinOPS query modules."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from config.settings import FILTER_ALL
from semantic.time_intelligence import resolve_time_window, sql_date_literal, time_bucket_sql


def normalize_selected(values: Sequence[str] | None) -> list[str]:
    """Return selected values excluding the All sentinel."""
    if not values:
        return []
    cleaned = [str(v) for v in values if str(v) != FILTER_ALL]
    return cleaned


def in_clause(column: str, values: Sequence[str] | None) -> str:
    """Build a safe IN clause or empty string when all values are selected."""
    selected = normalize_selected(values)
    if not selected:
        return ""
    quoted = ", ".join("'" + v.replace("'", "''") + "'" for v in selected)
    return f" AND {column} IN ({quoted})"


def date_clause(column: str, filters: dict[str, Any] | None) -> str:
    """Build a date range clause from filters."""
    start, end = resolve_time_window(filters)
    return f" AND {column} BETWEEN DATE '{sql_date_literal(start)}' AND DATE '{sql_date_literal(end)}'"


def common_where(
    column: str,
    filters: dict[str, Any] | None,
    business_column: str | None = None,
    environment_column: str | None = None,
) -> str:
    """Build a common WHERE tail with date, business line and environment filters."""
    clause = date_clause(column, filters)
    if filters and business_column:
        clause += in_clause(business_column, filters.get("selected_business_lines"))
    if filters and environment_column:
        clause += in_clause(environment_column, filters.get("selected_environments"))
    return clause


def cost_column(currency: str) -> str:
    """Return the numeric cost column matching the selected currency."""
    return "COST_USD" if str(currency).upper() == "USD" else "COST_EUR"


def bucket_expr(column: str, fmt: str) -> str:
    """Return a Snowflake bucket expression for month/quarter/year."""
    return time_bucket_sql(column, fmt)


def period_label(column: str, fmt: str) -> str:
    """Return a readable label for the selected period."""
    bucket = bucket_expr(column, fmt)
    fmt = (fmt or "MONTH").upper()
    if fmt == "YEAR":
        return f"TO_CHAR({bucket}, 'YYYY')"
    if fmt == "QUARTER":
        return f"TO_CHAR({bucket}, 'YYYY') || '-Q' || TO_CHAR({bucket}, 'Q')"
    return f"TO_CHAR({bucket}, 'YYYY-MM')"
