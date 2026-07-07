"""Queries de la página Compute."""

from __future__ import annotations

from typing import Any

import pandas as pd

from config.settings import FINOPS_DATABASE, FINOPS_SCHEMA
from db.connection import run_query_cached
from queries.base import bucket_expr, common_where, cost_column, period_label


def _table(name: str) -> str:
    return f"{FINOPS_DATABASE}.{FINOPS_SCHEMA}.{name}"


def get_compute_kpis(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Main compute KPI block."""
    col = cost_column(currency)
    sql = f"""
        WITH compute AS (
            SELECT
                COALESCE(SUM({col}), 0) AS compute_cost,
                COALESCE(SUM(CREDITS_USED), 0) AS credits_used,
                COALESCE(SUM(CREDITS_USED_COMPUTE), 0) AS credits_compute,
                COALESCE(SUM(CREDITS_USED_CLOUD_SERVICES), 0) AS credits_cloud
            FROM {_table('FCT_COMPUTE_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        ), warehouse AS (
            SELECT COUNT(DISTINCT WAREHOUSE_NAME) AS warehouse_count
            FROM {_table('FCT_WAREHOUSE_TAG_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters, 'BUSINESS_LINE', 'ENVIRONMENT')}
        )
        SELECT
            compute.*,
            warehouse.warehouse_count,
            CASE
                WHEN compute.credits_compute + compute.credits_cloud = 0 THEN NULL
                ELSE compute.credits_cloud / NULLIF(compute.credits_compute + compute.credits_cloud, 0)
            END AS cloud_ratio,
            CASE
                WHEN compute.credits_compute + compute.credits_cloud = 0 THEN NULL
                ELSE compute.credits_compute / NULLIF(compute.credits_compute + compute.credits_cloud, 0)
            END AS compute_ratio
        FROM compute, warehouse
    """
    return run_query_cached(sql)


def get_warehouse_ranking(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Ranking of warehouses by cost."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            f.WAREHOUSE_NAME,
            f.BUSINESS_LINE,
            f.ENVIRONMENT,
            f.LAYER,
            SUM(f.{col}) AS cost_value,
            SUM(f.CREDITS_DISTRIBUTED) AS distributed_credits
        FROM {_table('FCT_WAREHOUSE_TAG_COST')} f
        WHERE 1=1{common_where('f.USAGE_DATE', filters, 'f.BUSINESS_LINE', 'f.ENVIRONMENT')}
        GROUP BY 1, 2, 3, 4
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_compute_type_breakdown(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Breakdown by service type / compute category."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            SERVICE_TYPE,
            COMPUTE_CATEGORY,
            SUM({col}) AS cost_value,
            SUM(CREDITS_USED) AS credits_used
        FROM {_table('FCT_COMPUTE_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_compute_trend(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Trend by month and compute category."""
    col = cost_column(currency)
    fmt = str((filters or {}).get("format", "MONTH")).upper()
    bucket = bucket_expr("USAGE_DATE", fmt)
    label = period_label("USAGE_DATE", fmt)
    sql = f"""
        SELECT
            {bucket} AS period_start,
            {label} AS period_label,
            COMPUTE_CATEGORY,
            SUM({col}) AS cost_value,
            SUM(CREDITS_USED) AS credits_used,
            SUM(CREDITS_USED_COMPUTE) AS compute_credits,
            SUM(CREDITS_USED_CLOUD_SERVICES) AS cloud_credits
        FROM {_table('FCT_COMPUTE_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2, 3
        ORDER BY 1, 3
    """
    return run_query_cached(sql)


def get_daily_heatmap(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Daily cost series for heatmap / calendar views."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            USAGE_DATE,
            SUM({col}) AS cost_value,
            SUM(CREDITS_USED) AS credits_used
        FROM {_table('FCT_COMPUTE_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1
        ORDER BY 1
    """
    return run_query_cached(sql)


# Backwards-compatible alias expected by the package export
get_compute_daily_heatmap = get_daily_heatmap


def get_warehouse_tag_breakdown(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Warehouse cost attributed to business line/environment tags."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            WAREHOUSE_NAME,
            BUSINESS_LINE,
            ENVIRONMENT,
            LAYER,
            SUM({col}) AS cost_value,
            SUM(CREDITS_DISTRIBUTED) AS distributed_credits
        FROM {_table('FCT_WAREHOUSE_TAG_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters, 'BUSINESS_LINE', 'ENVIRONMENT')}
        GROUP BY 1, 2, 3, 4
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)
