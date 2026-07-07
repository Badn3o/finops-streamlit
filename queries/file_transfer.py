"""Queries de la página File Transfer."""

from __future__ import annotations

from typing import Any

import pandas as pd

from config.settings import FINOPS_DATABASE, FINOPS_SCHEMA
from db.connection import run_query_cached
from queries.base import bucket_expr, common_where, cost_column, period_label


def _table(name: str) -> str:
    return f"{FINOPS_DATABASE}.{FINOPS_SCHEMA}.{name}"


def get_transfer_kpis(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Main transfer KPI block."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            COALESCE(SUM(BYTES_TRANSFERRED_GB), 0) AS volume_gb,
            COALESCE(SUM({col}), 0) AS transfer_cost,
            COALESCE(SUM(CREDITS_BILLED), 0) AS billed_credits,
            COUNT(DISTINCT ROUTE_ID) AS route_count
        FROM {_table('FCT_DATA_TRANSFER')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
    """
    return run_query_cached(sql)


def get_transfer_route_ranking(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Ranking of transfer routes by cost."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            SOURCE_CLOUD,
            SOURCE_REGION,
            TARGET_CLOUD,
            TARGET_REGION,
            TRANSFER_TYPE,
            SUM(BYTES_TRANSFERRED_GB) AS volume_gb,
            SUM({col}) AS cost_value,
            SUM(CREDITS_BILLED) AS billed_credits
        FROM {_table('FCT_DATA_TRANSFER')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2, 3, 4, 5
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_transfer_trend(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Trend of transfer cost and volume by period."""
    col = cost_column(currency)
    fmt = str((filters or {}).get("format", "MONTH")).upper()
    bucket = bucket_expr("USAGE_DATE", fmt)
    label = period_label("USAGE_DATE", fmt)
    sql = f"""
        SELECT
            {bucket} AS period_start,
            {label} AS period_label,
            SUM(BYTES_TRANSFERRED_GB) AS volume_gb,
            SUM({col}) AS cost_value,
            SUM(CREDITS_BILLED) AS billed_credits
        FROM {_table('FCT_DATA_TRANSFER')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2
        ORDER BY 1
    """
    return run_query_cached(sql)


def get_transfer_flow(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Sankey-ready flow table: source -> target with value."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            SOURCE_CLOUD AS source,
            TARGET_CLOUD AS target,
            SUM({col}) AS cost_value,
            SUM(BYTES_TRANSFERRED_GB) AS volume_gb
        FROM {_table('FCT_DATA_TRANSFER')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)
