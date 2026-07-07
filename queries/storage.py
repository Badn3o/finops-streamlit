"""Queries de la página Storage."""

from __future__ import annotations

from typing import Any

import pandas as pd

from config.settings import FINOPS_DATABASE, FINOPS_SCHEMA
from db.connection import run_query_cached
from queries.base import bucket_expr, common_where, cost_column, period_label


def _table(name: str) -> str:
    return f"{FINOPS_DATABASE}.{FINOPS_SCHEMA}.{name}"


def get_storage_kpis(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Main storage KPI block."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            COALESCE(SUM({col}), 0) AS storage_cost,
            COALESCE(SUM(AVERAGE_DATABASE_BYTES), 0) / 1099511627776 AS database_tb,
            COALESCE(SUM(AVERAGE_FAILSAFE_BYTES), 0) / 1099511627776 AS failsafe_tb,
            COALESCE(SUM(TOTAL_BILLABLE_BYTES), 0) / 1099511627776 AS billable_tb
        FROM {_table('FCT_DATABASE_STORAGE')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
    """
    return run_query_cached(sql)


def get_database_ranking(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Ranking of databases by storage cost."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            d.DATABASE_NAME,
            SUM(s.{col}) AS cost_value,
            SUM(s.AVERAGE_DATABASE_BYTES) / 1099511627776 AS database_tb,
            SUM(s.AVERAGE_FAILSAFE_BYTES) / 1099511627776 AS failsafe_tb
        FROM {_table('FCT_DATABASE_STORAGE')} s
        LEFT JOIN {_table('DIM_DATABASE')} d
            ON s.DATABASE_ID = d.DATABASE_ID
        WHERE 1=1{common_where('s.USAGE_DATE', filters)}
        GROUP BY 1
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_storage_trend(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Trend of storage cost and TB by period."""
    col = cost_column(currency)
    fmt = str((filters or {}).get("format", "MONTH")).upper()
    bucket = bucket_expr("USAGE_DATE", fmt)
    label = period_label("USAGE_DATE", fmt)
    sql = f"""
        SELECT
            {bucket} AS period_start,
            {label} AS period_label,
            SUM({col}) AS cost_value,
            SUM(AVERAGE_DATABASE_BYTES) / 1099511627776 AS database_tb,
            SUM(AVERAGE_FAILSAFE_BYTES) / 1099511627776 AS failsafe_tb
        FROM {_table('FCT_DATABASE_STORAGE')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2
        ORDER BY 1
    """
    return run_query_cached(sql)


def get_storage_tag_breakdown(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Business line / environment / layer storage distribution."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            BUSINESS_LINE,
            ENVIRONMENT,
            LAYER,
            SUM({col}) AS cost_value,
            SUM(STORAGE_TB) AS storage_tb
        FROM {_table('FCT_BL_ENV_TAG_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters, 'BUSINESS_LINE', 'ENVIRONMENT')}
        GROUP BY 1, 2, 3
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_storage_monthly_tag_cost(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Monthly TAG cost table."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            TAG_NAME,
            DATE_TRUNC('month', USAGE_DATE) AS period_start,
            TO_CHAR(DATE_TRUNC('month', USAGE_DATE), 'YYYY-MM') AS period_label,
            SUM({col}) AS cost_value,
            SUM(STORAGE_TB) AS storage_tb
        FROM {_table('FCT_TAG_MONTHLY_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2, 3
        ORDER BY period_start, cost_value DESC
    """
    return run_query_cached(sql)
