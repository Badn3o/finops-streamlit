"""Time intelligence helpers for FinOPS queries."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from config.settings import DEFAULT_DATE_RANGE_MONTHS, FY_START_MONTH


def _as_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    raise TypeError(f"Unsupported date value: {value!r}")


def default_date_range() -> tuple[date, date]:
    """Default last-N-months window."""
    today = date.today()
    start = today - timedelta(days=30 * DEFAULT_DATE_RANGE_MONTHS)
    return start, today


def resolve_date_range(filters: dict[str, Any] | None) -> tuple[date, date]:
    """Resolve the active date range from filters or time intelligence defaults."""
    if not filters:
        return default_date_range()

    value = filters.get("date_range")
    if isinstance(value, tuple) and len(value) == 2:
        return _as_date(value[0]), _as_date(value[1])
    if isinstance(value, list) and len(value) == 2:
        return _as_date(value[0]), _as_date(value[1])
    return default_date_range()


def fiscal_year_bounds(reference: date | None = None) -> tuple[date, date]:
    """Return fiscal year start/end bounds for the current FY (Oct-Sep)."""
    ref = reference or date.today()
    start_year = ref.year if ref.month >= FY_START_MONTH else ref.year - 1
    start = date(start_year, FY_START_MONTH, 1)
    end = date(start_year + 1, FY_START_MONTH - 1, 1)
    return start, end


def resolve_time_window(filters: dict[str, Any] | None) -> tuple[date, date]:
    """Resolve the effective time window with priority: explicit range > time intelligence."""
    if not filters:
        return default_date_range()

    explicit = filters.get("date_range")
    if explicit:
        return resolve_date_range(filters)

    selection = str(filters.get("time_intelligence", "6 MTD")).upper()
    today = date.today()
    if selection in {"CURRENT", "MTD"}:
        return date(today.year, today.month, 1), today
    if selection == "6 MTD":
        return today - timedelta(days=183), today
    if selection == "YTD":
        return date(today.year, 1, 1), today
    if selection == "FYTD":
        return fiscal_year_bounds(today)[0], today
    return default_date_range()


def sql_date_literal(value: date) -> str:
    return value.isoformat()


def time_bucket_sql(column: str, fmt: str) -> str:
    """Return a Snowflake expression for bucketing dates by month/quarter/year."""
    fmt = (fmt or "MONTH").upper()
    if fmt == "YEAR":
        return f"DATE_TRUNC('year', {column})"
    if fmt == "QUARTER":
        return f"DATE_TRUNC('quarter', {column})"
    return f"DATE_TRUNC('month', {column})"


def period_label_sql(column: str, fmt: str) -> str:
    """Return a label expression consistent with the selected period."""
    bucket = time_bucket_sql(column, fmt)
    return f"TO_CHAR({bucket}, 'YYYY-MM')" if fmt.upper() == "MONTH" else f"TO_CHAR({bucket}, 'YYYY-MM-DD')"
